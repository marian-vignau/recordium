# Copyright 2016-2017 Facundo Batista
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://github.com/facundobatista/recordium

import json
import logging
import os
import uuid

from datetime import datetime
from urllib import parse

import defer

from PyQt5 import QtCore, QtNetwork

from recordium.config import config
from recordium.utils import data_basedir

logger = logging.getLogger(__name__)

API_BASE = "https://api.telegram.org/bot{token}/{method}"
API_FILE = "https://api.telegram.org/file/bot{token}/{file_path}"


class NotificationItem:
    """The item shown in the notification."""

    def __init__(self, text, sent_at, message_id, extfile_path):
        self.text = text
        self.sent_at = sent_at
        self.message_id = message_id
        self.extfile_path = extfile_path

    @classmethod
    @defer.inline_callbacks
    def from_update(cls, update):
        """Create from a telegram message."""
        update_id = int(update['update_id'])
        try:
            msg = update['message']
        except KeyError:
            logger.warning("Unknown update type: %r", update)
            return

        sent_at = datetime.fromtimestamp(msg['date'])

        if 'text' in msg:
            text = msg['text']
            extfile_path = None
        elif 'photo' in msg:
            # grab the content of the biggest photo only
            photo = max(msg['photo'], key=lambda photo: photo['width'])
            text = "<image, click to open>"
            extfile_path = yield download_file(photo['file_id'])
        defer.return_value(cls(
            text=text, sent_at=sent_at, message_id=update_id, extfile_path=extfile_path))

    def __str__(self):
        return "<Message [{}] {} {!r} ({!r})>".format(
            self.message_id, self.sent_at, self. text, self.extfile_path)


class NetworkError(Exception):
    """Problems in the network."""


class _Downloader(object):
    """An asynch downloader that fires a deferred with data when done."""

    def __init__(self, url, file_path=None):
        if file_path is None:
            self.file_handler = None
            self.file_downloaded_size = None
        else:
            self.file_handler = open(file_path, "wb")
            self.file_downloaded_size = 0

        self._qt_network_manager = QtNetwork.QNetworkAccessManager()

        self.deferred = defer.Deferred()
        self.deferred._store_it_because_qt_needs_or_wont_work = self
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))

        self.req = self._qt_network_manager.get(request)
        self.req.error.connect(self.error)
        self.req.finished.connect(self.end)
        if self.file_handler is not None:
            self.req.downloadProgress.connect(self._save_partial)

    def _save_partial(self, dloaded, total):
        """Save partially downloaded content."""
        new_data = self.req.readAll()
        self.file_downloaded_size += len(new_data)
        self.file_handler.write(new_data)

    def error(self, error_code):
        """Request finished (*maybe*) on error."""
        error_message = "Downloader error {}: {}".format(error_code, self.req.errorString())
        logger.warning(error_message)
        if not self.deferred.called:
            self.deferred.errback(NetworkError(error_message))

    def end(self):
        """Send data through the deferred, if wasn't fired before."""
        if self.file_handler is None:
            result = self.req.read(self.req.bytesAvailable())
        else:
            result = self.file_downloaded_size
            self.file_handler.close()

        if result and not self.deferred.called:
            self.deferred.callback(result)


def build_baseapi_url(method, **kwargs):
    """Build the proper url to hit the API."""
    token = config.get(config.BOT_AUTH_TOKEN)
    url = API_BASE.format(token=token, method=method)
    if kwargs:
        url += '?' + parse.urlencode(kwargs)
    return url


def build_fileapi_url(file_path):
    """Build the proper url to hit the API."""
    token = config.get(config.BOT_AUTH_TOKEN)
    url = API_FILE.format(token=token, file_path=file_path)
    return url


@defer.inline_callbacks
def download_file(file_id):
    """Download the file content from Telegram."""
    url = build_baseapi_url('getFile', file_id=file_id)
    logger.debug("Getting file path, file_id=%s", file_id)
    downloader = _Downloader(url)
    encoded_data = yield downloader.deferred

    logger.debug("getFile response encoded data len=%d", len(encoded_data))
    data = json.loads(encoded_data.decode('utf8'))
    if not data.get('ok'):
        logger.warning("getFile result is not ok: %s", encoded_data)
        return

    remote_path = data['result']['file_path']
    url = build_fileapi_url(remote_path)
    file_path = os.path.join(data_basedir, uuid.uuid4().hex + '-' + os.path.basename(remote_path))
    logger.debug("Getting file content, storing in %r", file_path)
    downloader = _Downloader(url, file_path)
    downloaded_size = yield downloader.deferred

    logger.debug("Downloaded file content, size=%d", downloaded_size)
    defer.return_value(file_path)


class MessagesGetter:
    """Get messages."""

    def __init__(self, new_items_callback, last_id_callback):
        self.new_items_callback = new_items_callback
        self.last_id_callback = last_id_callback

    @defer.inline_callbacks
    def _process(self, encoded_data):
        """Process received info."""
        logger.debug("Process encoded data len=%d", len(encoded_data))
        data = json.loads(encoded_data.decode('utf8'))
        if data.get('ok'):
            results = data['result']
            logger.debug("Telegram results ok! len=%d", len(results))
            items = []
            for item in results:
                logger.debug("Processing result: %s", item)
                ni = yield NotificationItem.from_update(item)
                if ni is not None:
                    items.append(ni)
            if items:
                self.new_items_callback(items)
        else:
            logger.warning("Telegram result is not ok: %s", data)

    def go(self):
        """Get the info from Telegram."""
        last_id = self.last_id_callback()
        kwargs = {}
        if last_id is not None:
            kwargs['offset'] = last_id + 1
        url = build_baseapi_url('getUpdates', **kwargs)
        logger.debug("Getting updates, kwargs=%s", kwargs)

        def _re_get(error):
            """Capture all results; always re-issue self.go, if error raise it."""
            polling_time = 1000 * config.get(config.POLLING_TIME)
            logger.debug("Re get, error=%s polling_time=%d", error, polling_time)
            QtCore.QTimer.singleShot(polling_time, self.go)
            if error is not None:
                error.raise_exception()

        self._downloader = _Downloader(url)
        self._downloader.deferred.add_callback(self._process)
        self._downloader.deferred.add_callbacks(_re_get, _re_get)

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

import logging
import subprocess
import sys
import platform
import os

from functools import lru_cache

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import __file__ as pyqt_path

from recordium import network, storage
from recordium.config import config

logger = logging.getLogger(__name__)

def fix_environment():
    """add enviroment variable on Windows systems"""

    if platform.system() == "Windows":
        pyqt = os.path.dirname(pyqt_path)
        qt_platform_plugins_path = os.path.join(pyqt, "plugins")
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_platform_plugins_path


# the text to show in the About window
ABOUT_TEXT = """
<center>
Send messages via Telegram that will be notified later in your desktop.<br/>
<br/>
Version {version}<br/>
<br/>
<small>Copyright 2016 Facundo Batista</small><br/>
<br/>
<a href="https://github.com/facundobatista/recordium">The project</a>
</center>
"""

# the text to build the systray menu
N_MESSAGES_TEXT = "{quantity} new messages"

# icons to show if there are messages or not
ICONPATH_NO_MESSAGE = 'media/icon-192.png'
ICONPATH_HAVE_MESSAGES = 'media/icon-active-192.png'
ICONPATH_PROBLEM = 'media/icon-problem-192.png'


def debug_trace():
    """Set a tracepoint in the Python debugger that works with Qt"""
    from PyQt5.QtCore import pyqtRemoveInputHook

    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()


class ConfigWidget(QtWidgets.QDialog):
    """The config window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration")

        main_layout = QtWidgets.QVBoxLayout()
        if not config.get(config.BOT_AUTH_TOKEN):
            main_layout.addWidget(QtWidgets.QLabel(
                "Please configure Recordium to be able to start fetching messages\n"
                "See instructions on README.rst"), 0)
            hline = QtWidgets.QFrame()
            hline.setFrameShape(QtWidgets.QFrame.HLine)
            hline.setFrameShadow(QtWidgets.QFrame.Sunken)
            main_layout.addWidget(hline)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel("Telegram bot auth token:"), 0, 0)
        prev = config.get(config.BOT_AUTH_TOKEN)
        self.entry_auth_token = QtWidgets.QLineEdit(prev)
        grid.addWidget(self.entry_auth_token, 0, 1)

        grid.addWidget(QtWidgets.QLabel("Polling time (in seconds, min=1)"), 1, 0)
        prev = config.get(config.POLLING_TIME)
        self.entry_polling_time = QtWidgets.QSpinBox()
        self.entry_polling_time.setValue(prev)
        self.entry_polling_time.setMinimum(1)
        grid.addWidget(self.entry_polling_time, 1, 1)

        main_layout.addLayout(grid, 0)

        self.setLayout(main_layout)
        self.show()

    def closeEvent(self, event):
        """Intercept closing and save config."""
        config.set(config.BOT_AUTH_TOKEN, self.entry_auth_token.text().strip())
        config.set(config.POLLING_TIME, self.entry_polling_time.value())
        config.save()
        super().closeEvent(event)


class MessagesWidget(QtWidgets.QTableWidget):
    """The list of messages."""

    # useful columns, to not use just numbers in the code
    text_col = 1
    check_col = 2

    def __init__(self, storage, systray):
        self._messages = storage.get_elements()
        self._storage = storage
        self._systray = systray
        super().__init__(len(self._messages), 3)

        for row, msg in enumerate(self._messages):
            item = QtWidgets.QTableWidgetItem(str(msg.sent_at))
            self.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(msg.text)
            self.setItem(row, 1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.setItem(row, self.check_col, item)

        self.setHorizontalHeaderLabels(("When", "Text", "Done"))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSizeAdjustPolicy(2)

        self.itemClicked.connect(self.item_clicked)
        self.show()

    def closeEvent(self, event):
        """Intercept closing and delete marked messages."""
        messages_to_remove = []
        for row in range(self.rowCount()):
            if self.item(row, self.check_col).checkState() == QtCore.Qt.Checked:
                # note, we can access the message like this because the table can not be reordered
                messages_to_remove.append(self._messages[row])
        if messages_to_remove:
            self._storage.delete_elements(messages_to_remove)
            self._systray.set_message_number()
        super().closeEvent(event)

    def item_clicked(self, widget):
        """An item in the table was clicked."""
        column = widget.column()
        if column == self.check_col:
            should_strikeout = widget.checkState() == QtCore.Qt.Checked
            row = widget.row()
            for column in range(2):
                item = self.item(row, column)
                font = item.font()
                font.setStrikeOut(should_strikeout)
                item.setFont(font)
        elif column == self.text_col:
            row = widget.row()
            msg = self._messages[row]
            if msg.extfile_path is not None:
                logger.debug("Opening external file %r", msg.extfile_path)
                subprocess.call(['/usr/bin/xdg-open', msg.extfile_path])


class SysTray:
    def __init__(self, app, version):
        self.app = app
        self.version = version

        # build the icon and message line, which will be properly set below when calling the
        # set_message_number() method
        self.sti = sti = QtWidgets.QSystemTrayIcon()
        self.menu = menu = QtWidgets.QMenu()
        self._messages_action = menu.addAction('')
        self.set_message_number()
        self._messages_action.triggered.connect(self._show_messages)

        menu.addSeparator()
        action = menu.addAction("Configure")
        action.triggered.connect(self._configure)
        action = menu.addAction("About")
        action.triggered.connect(self._about)
        action = menu.addAction("Quit")
        action.triggered.connect(lambda _: self.app.quit())
        sti.setContextMenu(menu)

        sti.show()

    def _configure(self, _):
        """Show the configuration dialog."""
        self._temp_cw = ConfigWidget()
        self._temp_cw.exec_()

    def _about(self, _):
        """Show the About dialog."""
        version = self.version if self.version else "(?)"
        title = "Recordium v" + version
        text = ABOUT_TEXT.format(version=version)
        QtWidgets.QMessageBox.about(None, title, text)

    def _show_messages(self, _):
        """Show a window with the messages."""
        # store it in the instance otherwise it's destroyed
        self._temp_mw = MessagesWidget(self.app.storage, self)

    @lru_cache(None)
    def _get_icon(self, have_messages):
        """Return and cache an icon."""
        if not config.get(config.BOT_AUTH_TOKEN):
            path = ICONPATH_PROBLEM
        elif have_messages:
            path = ICONPATH_HAVE_MESSAGES
        else:
            path = ICONPATH_NO_MESSAGE
        return QtGui.QIcon(path)

    def set_message_number(self):
        """Set the message number in the systray icon."""
        quantity = len(self.app.storage.get_elements())
        self._messages_action.setText(N_MESSAGES_TEXT.format(quantity=quantity))
        self.sti.setIcon(self._get_icon(bool(quantity)))
        self._messages_action.setEnabled(bool(quantity))


class RecordiumApp(QtWidgets.QApplication):
    def __init__(self, version):
        super().__init__(sys.argv)
        if not config.get(config.BOT_AUTH_TOKEN):
            self._temp_cw = ConfigWidget()
            self._temp_cw.exec_()
        self.setQuitOnLastWindowClosed(False)  # so app is not closed when closing other windows
        self.storage = storage.Storage()
        self.systray = SysTray(self, version)
        self.messages_getter = network.MessagesGetter(
            self._new_messages, self.storage.get_last_element_id)
        self.messages_getter.go()

    def _new_messages(self, messages):
        """Called when new messages are available."""
        self.storage.add_elements(messages)
        self.systray.set_message_number()


def go(version):
    fix_environment()
    app = RecordiumApp(version)
    sys.exit(app.exec_())

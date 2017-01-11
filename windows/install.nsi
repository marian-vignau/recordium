; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Recordium"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "publisher-team"
!define PRODUCT_WEB_SITE "https://github.com/facundobatista/recordium"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\main.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "..\media\recordium.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\main.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.rst"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SpanishInternational"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "Setup.exe"
InstallDir "$PROGRAMFILES\Recordium"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File "..\dist\main\api-ms-win-crt-conio-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-convert-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-environment-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-filesystem-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-heap-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-locale-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-math-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-multibyte-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-process-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-runtime-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-stdio-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-string-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-time-l1-1-0.dll"
  File "..\dist\main\api-ms-win-crt-utility-l1-1-0.dll"
  File "..\dist\main\base_library.zip"
  File "..\dist\main\icudt55.dll"
  File "..\dist\main\icuin55.dll"
  File "..\dist\main\icuuc55.dll"
  File "..\dist\main\LIBEAY32.dll"
  File "..\dist\main\mfc100u.dll"
  File "..\dist\main\MSVCP140.dll"
  File "..\dist\main\MSVCR100.dll"
  File "..\dist\main\pyexpat.cp35-win_amd64.pyd"
  File "..\dist\main\PyQt5.Qt.cp35-win_amd64.pyd"
  File "..\dist\main\PyQt5.QtCore.cp35-win_amd64.pyd"
  File "..\dist\main\PyQt5.QtGui.cp35-win_amd64.pyd"
  File "..\dist\main\PyQt5.QtNetwork.cp35-win_amd64.pyd"
  File "..\dist\main\PyQt5.QtPrintSupport.cp35-win_amd64.pyd"
  File "..\dist\main\PyQt5.QtWidgets.cp35-win_amd64.pyd"
  File "..\dist\main\python35.dll"
  File "..\dist\main\pythoncom35.dll"
  File "..\dist\main\pywintypes35.dll"
  File "..\dist\main\Qt5Core.dll"
  File "..\dist\main\Qt5Gui.dll"
  File "..\dist\main\Qt5Network.dll"
  File "..\dist\main\Qt5PrintSupport.dll"
  File "..\dist\main\Qt5Widgets.dll"
  File "..\dist\main\main.exe"
  CreateDirectory "$SMPROGRAMS\Recordium"
  CreateShortCut "$SMPROGRAMS\Recordium\Recordium.lnk" "$INSTDIR\main.exe"
  CreateShortCut "$DESKTOP\Recordium.lnk" "$INSTDIR\main.exe"
  File "..\dist\main\select.cp35-win_amd64.pyd"
  File "..\dist\main\sip.cp35-win_amd64.pyd"
  File "..\dist\main\SSLEAY32.dll"
  File "..\dist\main\unicodedata.cp35-win_amd64.pyd"
  File "..\dist\main\VCRUNTIME140.dll"
  File "..\dist\main\win32api.cp35-win_amd64.pyd"
  File "..\dist\main\win32com.shell.shell.cp35-win_amd64.pyd"
  File "..\dist\main\win32trace.cp35-win_amd64.pyd"
  File "..\dist\main\win32ui.cp35-win_amd64.pyd"
  File "..\dist\main\win32wnet.cp35-win_amd64.pyd"
  File "..\dist\main\_bz2.cp35-win_amd64.pyd"
  File "..\dist\main\_ctypes.cp35-win_amd64.pyd"
  File "..\dist\main\_hashlib.cp35-win_amd64.pyd"
  File "..\dist\main\_lzma.cp35-win_amd64.pyd"
  File "..\dist\main\_socket.cp35-win_amd64.pyd"
  File "..\dist\main\_ssl.cp35-win_amd64.pyd"
  File "..\dist\main\_win32sysloader.cp35-win_amd64.pyd"
  SetOverwrite ifnewer
  File "..\README.rst"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\Recordium\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\Recordium\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\main.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\main.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure to remove all $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\README.rst"
  Delete "$INSTDIR\_win32sysloader.cp35-win_amd64.pyd"
  Delete "$INSTDIR\_ssl.cp35-win_amd64.pyd"
  Delete "$INSTDIR\_socket.cp35-win_amd64.pyd"
  Delete "$INSTDIR\_lzma.cp35-win_amd64.pyd"
  Delete "$INSTDIR\_hashlib.cp35-win_amd64.pyd"
  Delete "$INSTDIR\_ctypes.cp35-win_amd64.pyd"
  Delete "$INSTDIR\_bz2.cp35-win_amd64.pyd"
  Delete "$INSTDIR\win32wnet.cp35-win_amd64.pyd"
  Delete "$INSTDIR\win32ui.cp35-win_amd64.pyd"
  Delete "$INSTDIR\win32trace.cp35-win_amd64.pyd"
  Delete "$INSTDIR\win32com.shell.shell.cp35-win_amd64.pyd"
  Delete "$INSTDIR\win32api.cp35-win_amd64.pyd"
  Delete "$INSTDIR\VCRUNTIME140.dll"
  Delete "$INSTDIR\unicodedata.cp35-win_amd64.pyd"
  Delete "$INSTDIR\SSLEAY32.dll"
  Delete "$INSTDIR\sip.cp35-win_amd64.pyd"
  Delete "$INSTDIR\select.cp35-win_amd64.pyd"
  Delete "$INSTDIR\main.exe"
  Delete "$INSTDIR\Qt5Widgets.dll"
  Delete "$INSTDIR\Qt5PrintSupport.dll"
  Delete "$INSTDIR\Qt5Network.dll"
  Delete "$INSTDIR\Qt5Gui.dll"
  Delete "$INSTDIR\Qt5Core.dll"
  Delete "$INSTDIR\pywintypes35.dll"
  Delete "$INSTDIR\pythoncom35.dll"
  Delete "$INSTDIR\python35.dll"
  Delete "$INSTDIR\PyQt5.QtWidgets.cp35-win_amd64.pyd"
  Delete "$INSTDIR\PyQt5.QtPrintSupport.cp35-win_amd64.pyd"
  Delete "$INSTDIR\PyQt5.QtNetwork.cp35-win_amd64.pyd"
  Delete "$INSTDIR\PyQt5.QtGui.cp35-win_amd64.pyd"
  Delete "$INSTDIR\PyQt5.QtCore.cp35-win_amd64.pyd"
  Delete "$INSTDIR\PyQt5.Qt.cp35-win_amd64.pyd"
  Delete "$INSTDIR\pyexpat.cp35-win_amd64.pyd"
  Delete "$INSTDIR\MSVCR100.dll"
  Delete "$INSTDIR\MSVCP140.dll"
  Delete "$INSTDIR\mfc100u.dll"
  Delete "$INSTDIR\main.exe.manifest"
  Delete "$INSTDIR\LIBEAY32.dll"
  Delete "$INSTDIR\icuuc55.dll"
  Delete "$INSTDIR\icuin55.dll"
  Delete "$INSTDIR\icudt55.dll"
  Delete "$INSTDIR\base_library.zip"
  Delete "$INSTDIR\api-ms-win-crt-utility-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-time-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-string-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-stdio-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-runtime-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-process-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-multibyte-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-math-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-locale-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-heap-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-filesystem-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-environment-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-convert-l1-1-0.dll"
  Delete "$INSTDIR\api-ms-win-crt-conio-l1-1-0.dll"

  Delete "$SMPROGRAMS\Recordium\Uninstall.lnk"
  Delete "$SMPROGRAMS\Recordium\Website.lnk"
  Delete "$DESKTOP\Recordium.lnk"
  Delete "$SMPROGRAMS\Recordium\Recordium.lnk"

  RMDir "$SMPROGRAMS\Recordium"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd
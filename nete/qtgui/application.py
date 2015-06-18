from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQml import (qmlRegisterType, qmlRegisterSingletonType,
                         QQmlEngine)
from nete.qtgui.main_window import MainWindowBuilder
from nete.qtgui.tray_icon import TrayIcon
from nete.qtgui.qmltypes.qml_note_storage import QmlNoteStorage
from nete.services.markdown_renderer import MarkdownRenderer


class Application(QApplication):

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self.setOrganizationName('nete')
        self.setApplicationName('nete-qt')

        self._init_qml_engine()

        self._note_storage = QmlNoteStorage(parent=self)

        self._main_window = MainWindowBuilder(self.qml_engine).build(self._note_storage)

        self._tray_icon = TrayIcon(self)
        self._tray_icon.activated.connect(self.tray_icon_activated)
        self._tray_icon.show()

        self.aboutToQuit.connect(self.stopServices)

    def stopServices(self):
        # TODO somehow do this automatically, like onDestroy, but how?
        self._note_storage.close()

    def tray_icon_activated(self, reason):
        if reason == TrayIcon.Trigger:
            self._main_window.setVisibility(not self._main_window.isVisible())

    def _init_qml_engine(self):
        self.qml_engine = QQmlEngine()

        qmlRegisterType(QmlNoteStorage, 'nete', 1, 0, 'NoteStorage')
        qmlRegisterSingletonType(MarkdownRenderer, 'nete', 1, 0, 'MarkdownRenderer', self._make_renderer)

    def _make_renderer(self, *args):
        return MarkdownRenderer()

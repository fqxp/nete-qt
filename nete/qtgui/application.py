from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQml import (qmlRegisterType, qmlRegisterSingletonType,
                         QQmlApplicationEngine)
from nete.qtgui.main_window_builder import MainWindowBuilder
from nete.qtgui.tray_icon import TrayIcon
from nete.qtgui.qmltypes.qml_note_list_model import QmlNoteListModel
from nete.services.markdown_renderer import MarkdownRenderer


class Application(QApplication):

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self.setOrganizationName('nete')
        self.setApplicationName('nete-qt')

        self._init_qml_engine()

        self._main_window = MainWindowBuilder(self.qml_engine).build()
        self._main_window.show()

        self._tray_icon = TrayIcon(self)
        self._tray_icon.activated.connect(self.tray_icon_activated)
        self._tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == TrayIcon.Trigger:
            self._main_window.setVisibility(not self._main_window.isVisible())

    def _init_qml_engine(self):
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.quit.connect(self.quit)

        qmlRegisterType(QmlNoteListModel, 'nete', 1, 0, 'NoteList')
        qmlRegisterSingletonType(MarkdownRenderer, 'nete', 1, 0, 'MarkdownRenderer', self._make_renderer)

    def _make_renderer(self, *args):
        return MarkdownRenderer()

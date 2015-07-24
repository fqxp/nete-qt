from PyQt5.QtDBus import QDBusConnection
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQml import qmlRegisterType, qmlRegisterSingletonType, QQmlApplicationEngine
from nete.qtgui.main_controller_builder import MainControllerBuilder
from nete.qtgui.tray_icon import TrayIcon
from nete.qtgui.qmltypes.qml_note_list_model import QmlNoteListModel
from nete.qtgui.dbus_interface import MainControllerAdaptor
from nete.services.markdown_renderer import MarkdownRenderer


class Application(QApplication):

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self.setOrganizationName('nete')
        self.setApplicationName('nete-qt')

        self.init_qml_engine()

        self._main_controller = MainControllerBuilder(self.qml_engine).build()
        self._main_controller_adaptor = MainControllerAdaptor(self._main_controller)

        self._tray_icon = TrayIcon(self)
        self._tray_icon.activated.connect(self.tray_icon_activated)
        self._tray_icon.show()

        self.register_dbus_interface()

    def register_dbus_interface(self):
        connection = QDBusConnection.sessionBus()
        connection.registerObject('/', self._main_controller)
        connection.registerService('de.fqxp.nete')

    def tray_icon_activated(self, reason):
        if reason == TrayIcon.Trigger:
            self._main_controller.toggle()

    def init_qml_engine(self):
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.quit.connect(self.quit)

        qmlRegisterType(QmlNoteListModel, 'nete', 1, 0, 'NoteList')
        qmlRegisterSingletonType(MarkdownRenderer, 'nete', 1, 0, 'MarkdownRenderer', self.make_renderer)

    def make_renderer(self, *args):
        return MarkdownRenderer()


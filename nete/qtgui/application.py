from PyQt5.QtDBus import QDBusConnection
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import qmlRegisterType, qmlRegisterSingletonType, QQmlApplicationEngine
from nete.qtgui.main_controller_builder import MainControllerBuilder
from nete.qtgui.tray_icon import TrayIcon
from nete.qtgui.qmltypes.qml_note_list_model import QNoteListModelFactory
from nete.qtgui.dbus_interface import MainControllerAdaptor
from nete.services.markdown_renderer import MarkdownRenderer
import sys


class Application(QApplication):

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self.setOrganizationName('nete')
        self.setApplicationName('nete-qt')

        self.init_qml_engine()

        self.main_controller = MainControllerBuilder(self.qml_engine).build()
        self.main_controller_adaptor = MainControllerAdaptor(self.main_controller)

        self.tray_icon = TrayIcon(self.main_controller)
        self.tray_icon.show()

        self.register_dbus_interface()

    def init_qml_engine(self):
        self.qml_engine = QQmlApplicationEngine()
        self.qml_engine.quit.connect(self.quit)

        #qmlRegisterType(QmlNoteListModel, 'nete', 1, 0, 'NoteList')
        qmlRegisterSingletonType(MarkdownRenderer, 'nete', 1, 0, 'MarkdownRenderer', self.make_renderer)
        qmlRegisterSingletonType(QNoteListModelFactory, 'nete', 1, 0, 'NoteListModelFactory', self.make_note_list_model_factory)

    def register_dbus_interface(self):
        connection = QDBusConnection.sessionBus()
        connection.registerObject('/', self.main_controller)
        connection.registerService('de.fqxp.nete')

    def make_renderer(self, *args):
        return MarkdownRenderer()

    def make_note_list_model_factory(self, parent=None, *args):
        factory = QNoteListModelFactory(parent=parent)
        return factory


def main():
    #import profile
    #profile.run('sys.exit(app.exec_())')

    app = Application(sys.argv)

    sys.exit(app.exec_())

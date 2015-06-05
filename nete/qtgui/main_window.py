import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import qmlRegisterType, qmlRegisterSingletonType, QQmlEngine, QQmlComponent
from nete.qtgui.qmltypes.qml_note_storage import QmlNoteStorage
#from nete.note import Note
#from nete.note_storage import NoteStorage
from nete.services.markdown_renderer import MarkdownRenderer
import os.path


class MainWindow(object):

    APP_QML = os.path.join(os.path.dirname(__file__), 'qml/MainWindow.qml')

    def __init__(self):
        self._engine = QQmlEngine()

        qmlRegisterType(QmlNoteStorage, 'nete', 1, 0, 'NoteStorage')
        qmlRegisterSingletonType(MarkdownRenderer, 'nete', 1, 0, 'MarkdownRenderer', self._make_renderer)

    def show(self):
        self._view = self._create_component()
        self._view.show()

    def _create_component(self):
        component = QQmlComponent(self._engine, QUrl(self.APP_QML))

        for error in component.errors():
            print 'QML error: %s' % error.toString()

        return component.create()

    def _make_renderer(self, *args):
        return MarkdownRenderer()



#if __name__ == '__main__':
#    app = QGuiApplication(sys.argv)
#
#    qmlRegisterType(Note, 'nete', 1, 0, 'Note')
#    qmlRegisterType(NoteStorage, 'nete', 1, 0, 'NoteStorage')
#    qmlRegisterSingletonType(MarkdownRenderer, 'nete', 1, 0, 'MarkdownRenderer', make_renderer)
#
#    view = open_window()
#
#    sys.exit(app.exec_())

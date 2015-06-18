import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlComponent, QQmlContext
import os.path


class MainWindowBuilder(object):

    APP_QML = os.path.join(os.path.dirname(__file__), 'qml/MainWindow.qml')

    def __init__(self, qml_engine):
        self._engine = qml_engine

    def build(self, note_storage):
        component = QQmlComponent(self._engine, QUrl(self.APP_QML))

        for error in component.errors():
            print 'QML error: %s' % error.toString()

        main_window = component.create()
        main_window.setProperty('noteStorage', note_storage)

        return main_window

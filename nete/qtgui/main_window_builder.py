import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlComponent
import os.path


class MainWindowBuilder(object):

    APP_QML = os.path.join(os.path.dirname(__file__), 'qml/MainWindow.qml')

    def __init__(self, qml_engine):
        self._engine = qml_engine

    def build(self):
        self._engine.load(QUrl(self.APP_QML))

        main_window = self._engine.rootObjects()[0]

        return main_window

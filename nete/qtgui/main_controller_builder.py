import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlComponent
import os.path


class MainControllerBuilder(object):

    MAIN_CONTROLLER_QML = os.path.join(os.path.dirname(__file__), 'qml/main_controller.qml')

    def __init__(self, qml_engine):
        self._engine = qml_engine

    def build(self):
        self._engine.load(QUrl(self.MAIN_CONTROLLER_QML))

        main_controller = self._engine.rootObjects()[0]

        return main_controller

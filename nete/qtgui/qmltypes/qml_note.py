from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class QmlNote(QObject):
    textChanged = pyqtSignal(name='textChanged')
    titleChanged = pyqtSignal(name='titleChanged')

    def __init__(self, parent=None):
        super(QmlNote, self).__init__(parent)
        self._id = None
        self.title = ''
        self.text = ''

    @pyqtProperty(str)
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.titleChanged.emit()

    @pyqtProperty(unicode, notify=textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.textChanged.emit()

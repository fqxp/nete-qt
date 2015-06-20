from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from nete.models.note import Note


class QmlNote(QObject):
    textChanged = pyqtSignal(name='textChanged')
    titleChanged = pyqtSignal(name='titleChanged')

    def __init__(self, note, parent=None):
        super(QmlNote, self).__init__(parent)
        self._note = note

    @property
    def note(self):
        return self._note

    @pyqtSlot()
    def save(self):
        self.parent().save(self)

    @pyqtProperty(str)
    def id(self):
        return self._note.id

    @id.setter
    def id(self, id):
        self._note.id = id

    @pyqtProperty(str, notify=titleChanged)
    def title(self):
        return self._note.title

    @title.setter
    def title(self, title):
        self._note.title = title
        self.titleChanged.emit()

    @pyqtProperty(unicode, notify=textChanged)
    def text(self):
        return self._note.text

    @text.setter
    def text(self, text):
        self._note.text = text
        self.textChanged.emit()

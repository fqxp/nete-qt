from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtQml import QQmlListProperty
from .qml_note import QmlNote
from nete.services.filesystem_note_storage import FilesystemNoteStorage
import json
import os
import os.path


class QmlNoteStorage(QObject):
    NOTE_DIR = './notes'

    noteListUpdated = pyqtSignal(QVariant, arguments=['notes'])
    noteLoaded = pyqtSignal(QVariant, arguments=['note'])

    def __init__(self, parent=None):
        super(QmlNoteStorage, self).__init__(parent)
        self._storage = FilesystemNoteStorage(self.NOTE_DIR, self.create)

    @pyqtSlot()
    def list(self):
        notes = self._storage.list()
        self.noteListUpdated.emit(QVariant(notes))

    @pyqtSlot('QString', result=QmlNote)
    def load(self, note_id):
        self._storage.load(note_id)
        self.noteLoaded.emit(QVariant(note))

    @pyqtSlot(QmlNote)
    def save(self, note):
        self._storage.save(note)

    def create(self):
        return QmlNote(parent=self)

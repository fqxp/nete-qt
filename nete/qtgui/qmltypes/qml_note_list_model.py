from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QVariant, QAbstractListModel, QModelIndex
from PyQt5.QtQml import QQmlListProperty
from .qml_note import QmlNote
from nete.services.filesystem_note_storage import FilesystemNoteStorage


import sys
import threading
import time


class QmlNoteListModel(QAbstractListModel):

    NOTE_DIR = './notes'

    IdRole = Qt.UserRole + 1
    TitleRole = Qt.UserRole + 2
    TextRole = Qt.UserRole + 3

    noteCreated = pyqtSignal(QmlNote, int, arguments=['note', 'row'])

    def __init__(self, qml_notes=None, parent=None):
        super(QmlNoteListModel, self).__init__(parent)
        self._storage = FilesystemNoteStorage(self.NOTE_DIR)
        self._notes = qml_notes

    def rowCount(self, parent=QModelIndex()):
        return len(self._notes)

    def data(self, index, role=Qt.DisplayRole):
        note = self._notes[index.row()]
        if role == self.IdRole:
            return note.id
        elif role == self.TitleRole:
            return note.title
        elif role == self.TextRole:
            return note.text

    def roleNames(self):
        return {
            Qt.DisplayRole: 'display',
            self.IdRole: 'id',
            self.TitleRole: 'title',
            self.TextRole: 'text',
        }

    @pyqtSlot()
    def load(self):
        notes = self._storage.list()
        self._notes = [QmlNote(note, parent=self) for note in notes]

    @pyqtSlot('QString', result=QmlNote)
    def note(self, note_id):
        return filter(
                lambda note: note.id == note_id,
                self._notes)[0]

    @pyqtSlot(QmlNote)
    def save(self, qml_note):
        self._storage.save(qml_note.note)

    @pyqtSlot()
    def create(self):
        note = QmlNote(self._storage.create(), parent=self)
        note.title = 'Unnamed'

        row = 0
        self.beginInsertRows(QModelIndex(), row, row)
        self._notes.insert(row, note)
        self.endInsertRows()

        self.noteCreated.emit(note, row)


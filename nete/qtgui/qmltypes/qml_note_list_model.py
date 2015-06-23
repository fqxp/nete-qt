from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QVariant, QAbstractListModel, QModelIndex
from PyQt5.QtQml import QQmlListProperty
from .qml_note import QmlNote
from nete.services.filesystem_note_storage import FilesystemNoteStorage


class QmlNoteListModel(QAbstractListModel):

    NOTE_DIR = './notes'

    IdRole = Qt.UserRole + 1
    TitleRole = Qt.UserRole + 2

    noteCreated = pyqtSignal(QmlNote, int, arguments=['note', 'row'])

    def __init__(self, parent=None):
        super(QmlNoteListModel, self).__init__(parent)
        self._storage = FilesystemNoteStorage(self.NOTE_DIR)
        self._notes = None

    @property
    def notes(self):
        if self._notes is None:
            self._load()
        return self._notes

    def _load(self):
        notes = self._storage.list()
        self._notes = []
        for note in notes:
            qml_note = QmlNote(note, parent=self)
            qml_note.titleChanged.connect(self._noteTitleChanged)
            self._notes.append(qml_note)

    @pyqtSlot()
    def _noteTitleChanged(self):
        index = self._notes.index(self.sender())
        self.dataChanged.emit(self.createIndex(index, 0),
                              self.createIndex(index, 0),
                              [self.TitleRole])

    def rowCount(self, parent=QModelIndex()):
        return len(self.notes)

    def data(self, index, role=Qt.DisplayRole):
        note = self.notes[index.row()]
        if role == self.IdRole:
            return note.id
        elif role == self.TitleRole:
            return note.title

    def roleNames(self):
        return {
            Qt.DisplayRole: 'display',
            self.IdRole: 'id',
            self.TitleRole: 'title',
        }

    @pyqtSlot('QString', result=QmlNote)
    def note(self, note_id):
        return filter(
                lambda note: note.id == note_id,
                self.notes)[0]

    @pyqtSlot(QmlNote)
    def save(self, qml_note):
        self._storage.save(qml_note.note)

    @pyqtSlot()
    def create(self):
        note = QmlNote(self._storage.create(), parent=self)
        note.title = 'Unnamed'

        row = 0
        self.beginInsertRows(QModelIndex(), row, row)
        self.notes.insert(row, note)
        self.endInsertRows()

        self.noteCreated.emit(note, row)


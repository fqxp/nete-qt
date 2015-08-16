from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant, QAbstractListModel, QModelIndex
from PyQt5.QtQml import QQmlListProperty
from .qml_note import QmlNote
from nete.models.nete_uri import NeteUri
from nete.services.storage_factory import StorageFactory


class QmlNoteListModel(QAbstractListModel):

    IdRole = Qt.UserRole + 1
    TitleRole = Qt.UserRole + 2

    noteCreated = pyqtSignal(QmlNote, int, arguments=['note', 'row'])

    def __init__(self, storage, parent=None):
        super(QmlNoteListModel, self).__init__(parent)
        self._storage = storage
        self._notes = None
        self._filter_expr = ''
        self._load()

    def rowCount(self, parent=QModelIndex()):
        return len(self._filtered_notes)

    def data(self, index, role=Qt.DisplayRole):
        note = self._filtered_notes[index.row()]
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
                self._notes)[0]

    @pyqtSlot(int, result=QmlNote)
    def noteAt(self, index):
        return self._filtered_notes[index]

    @pyqtSlot(QmlNote)
    def save(self, qml_note):
        self._storage.save(qml_note.note)

    @pyqtSlot()
    def create(self):
        note = QmlNote(self._storage.create(), parent=self)
        note.title = 'Unnamed'

        row = 0
        self.beginInsertRows(QModelIndex(), row, row)
        self._filtered_notes.insert(row, note)
        self.endInsertRows()

        note.titleChanged.connect(self._noteTitleChanged)

        self.save(note)
        self.noteCreated.emit(note, row)

    @pyqtSlot(QmlNote)
    def delete(self, qml_note):
        self._storage.delete(qml_note)

        row = self._notes.index(qml_note)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._notes[row]
        self.endRemoveRows()

        self._update_filtered_notes()

    @pyqtSlot(str)
    def setFilter(self, filter_expr):
        self._filter_expr = filter_expr
        self._update_filtered_notes()

    def _load(self):
        notes = self._storage.list()
        self._notes = []
        for note in notes:
            qml_note = QmlNote(note, parent=self)
            qml_note.titleChanged.connect(self._noteTitleChanged)
            self._notes.append(qml_note)

        self.beginResetModel()
        self._filtered_notes = self._sort_notes(self._notes)
        self.endResetModel()

    @pyqtSlot()
    def _noteTitleChanged(self):
        changed_note = self.sender()
        src_index = self._filtered_notes.index(changed_note)
        dest_index = next((i
                           for (i, note) in enumerate(self._filtered_notes)
                           if self._sort_key_fn(note) > self._sort_key_fn(changed_note)),
                          len(self._filtered_notes))

        if dest_index - 1 == src_index:
            new_qmodel_index = self.createIndex(src_index, 0)
            self.dataChanged.emit(new_qmodel_index, new_qmodel_index, [self.TitleRole])
            return

        self.beginMoveRows(QModelIndex(), src_index, src_index, QModelIndex(), dest_index)
        self._filtered_notes.insert(dest_index, changed_note)
        if src_index > dest_index:
            src_index += 1
        del self._filtered_notes[src_index]
        self.endMoveRows()

        new_qmodel_index = self.createIndex(dest_index if dest_index < src_index else dest_index - 1, 0)
        self.dataChanged.emit(new_qmodel_index, new_qmodel_index, [self.TitleRole])

    def _sort_notes(self, notes):
        return sorted(notes, key=self._sort_key_fn)

    def _filter_notes(self, unfiltered_notes):
        filter_fn = lambda note: (
            self._filter_expr == '' or
            self._filter_expr.lower() in note.title.lower())

        return filter(filter_fn, self._notes)

    def _update_filtered_notes(self):
        filtered_notes = self._sort_notes(self._filter_notes(self._notes))
        start = 0
        missing_notes = []

        # remove notes
        while True:
            if len(filtered_notes) == 0:
                self.beginRemoveRows(QModelIndex(), start, len(self._filtered_notes))
                del self._filtered_notes[start:]
                self.endRemoveRows()
                break

            next_note = filtered_notes.pop(0)

            try:
                end = self._filtered_notes.index(next_note)
                if start < end:
                    self.beginRemoveRows(QModelIndex(), start, end - 1)
                    del self._filtered_notes[start:end]
                    self.endRemoveRows()
                start += 1
            except ValueError:
                missing_notes.append(next_note)

        # add notes
        index = len(self._filtered_notes)
        while True:
            if len(missing_notes) == 0:
                break

            next_note = missing_notes.pop()

            while (index > 0 and
                   self._sort_key_fn(next_note) < self._sort_key_fn(self._filtered_notes[index - 1])):
                index -= 1

            self.beginInsertRows(QModelIndex(), index, index)
            self._filtered_notes.insert(index, next_note)
            self.endInsertRows()

    def _sort_key_fn(self, note):
        return note.title.lower()


class QmlNoteListModelFactory(QObject):

    @pyqtSlot('QString', result='QVariant')
    def create(self, nete_uri):
        nete_uri = NeteUri(nete_uri)
        storage = StorageFactory.create_storage(nete_uri)
        return QmlNoteListModel(storage, parent=self)


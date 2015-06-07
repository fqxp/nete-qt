from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QVariant, QAbstractListModel, QModelIndex
from PyQt5.QtQml import QQmlListProperty
from .qml_note import QmlNote
from nete.services.filesystem_note_storage import FilesystemNoteStorage


import sys
import threading
import time

class LazySaver(threading.Thread):

    def __init__(self, delay, max_delay, signal):
        super(LazySaver, self).__init__()
        self._delay = delay
        self._max_delay = max_delay
        self._signal = signal
        self._stopped = False
        self._qml_note = None
        self._condition = threading.Condition()
        self._counter = 0

    def stop(self):
        self._stopped = True
        self._condition.acquire()
        self._condition.notify()
        self._condition.release()

    def run(self):
        while True:
            print 'Waiting ...'
            self._condition.acquire()
            self._condition.wait()
            self._condition.release()

            if self._stopped:
                break

            if self._note is not None:
                print 'note saveeee %r ...' % (self._qml_note)
                self._save(self._qml_note)
                self._signal.emit(self._qml_note)
            self._qml_note = None

    def lazy_save(self, qml_note):
        self._condition.acquire()
        self._qml_note = qml_note
        self._condition.notify()
        self._condition.release()

    def _save(self, qml_note):
      print '-> %d' % self._counter
      qml_note.save()
      self._counter +=  1


class QmlNoteListModel(QAbstractListModel):
    def __init__(self, qml_notes=[], parent=None):
        super(QmlNoteListModel, self).__init__(parent)
        self._notes = qml_notes

    def rowCount(self, parent=QModelIndex()):
        return len(self._notes)

    def data(self, index, role=Qt.DisplayRole):
        return self._notes[index.row()]

    def roleNames(self):
        return {
            Qt.DisplayRole: 'display'
        }

    @pyqtSlot('QVariant', result=int)
    def add(self, note):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._notes.insert(0, note)
        self.endInsertRows()
        return 0


class QmlNoteStorage(QObject):
    NOTE_DIR = './notes'

    noteListUpdated = pyqtSignal(QVariant, arguments=['notes'])
    noteLoaded = pyqtSignal(QVariant, arguments=['note'])
    noteSaved = pyqtSignal(QVariant, arguments=['note'])

    def __init__(self, parent=None):
        super(QmlNoteStorage, self).__init__(parent)
        self._storage = FilesystemNoteStorage(self.NOTE_DIR)
        self._lazy_saver = LazySaver(2, 5, self.noteSaved)
        self._lazy_saver.start()

    @pyqtSlot()
    def close(self):
        self._lazy_saver.stop()

    @pyqtSlot()
    def list(self):
        notes = self._storage.list()
        qml_notes = QmlNoteListModel(
            [QmlNote(note, parent=self) for note in notes],
            parent=self)
        self.noteListUpdated.emit(qml_notes)

    @pyqtSlot('QString')
    def load(self, note_id):
        self._storage.load(note_id)
        self.noteLoaded.emit(QVariant(QmlNote(note, parent=self)))

    @pyqtSlot(result=QmlNote)
    def create(self):
        note = self._storage.create()
        note.title = "Unnamed"
        return QmlNote(note, parent=self)

    @pyqtSlot(QmlNote)
    def save(self, qml_note):
        self._storage.save(qml_note.note)

    @pyqtSlot(QmlNote)
    def lazy_save(self, qml_note):
        self._lazy_saver.lazy_save(qml_note)

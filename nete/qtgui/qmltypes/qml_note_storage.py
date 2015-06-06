from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QVariant
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
        qml_notes = [QmlNote(note, parent=self)
                     for note in notes]
        self.noteListUpdated.emit(QVariant(qml_notes))

    @pyqtSlot('QString', result=QmlNote)
    def load(self, note_id):
        self._storage.load(note_id)
        self.noteLoaded.emit(QVariant(QmlNote(note, parent=self)))

    @pyqtSlot(QmlNote)
    def save(self, qml_note):
        self._storage.save(qml_note.note)

    @pyqtSlot(QmlNote)
    def lazy_save(self, qml_note):
        self._lazy_saver.lazy_save(qml_note)

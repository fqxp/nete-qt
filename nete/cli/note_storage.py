class NoteStorage(object):

    def __init__(self):
        self._storage = FilesystemNoteStorage(self.NOTE_DIR, self.create)

    def create(self):
        return Note()

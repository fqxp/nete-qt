from nete.models.note import Note
import glob
import json
import os.path


class FilesystemNoteStorage(object):

    def __init__(self, note_dir):
        self._note_dir = note_dir

    def list(self):
        notes = [
            self.load(self._id_from_filename(os.path.basename(filename)))
            for filename in glob.glob(os.path.join(self._note_dir, '*.md'))
        ]

        return notes

    def load(self, note_id):
        note = Note()
        note.id = note_id

        with open(self._filename_from_id(note_id)) as fd:
            content = json.load(fd)
            note.title = content['title']
            note.text = content['text']

        return note

    def save(self, note):
        print "Saving note %s" % note.id

        with open(self._filename_from_id(note.id), 'w') as fd:
            content = {
                'title': note.title,
                'text': note.text,
            }
            json.dump(content, fd)

    def _filename_from_id(self, id):
        return os.path.join('notes', '%s.md' % id)

    def _id_from_filename(self, filename):
        return filename[:-3]

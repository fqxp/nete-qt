import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.1
import nete 1.0

Window {
    width: 640
    height: 400

    onClosing: {
        noteStorage.close();
    }

    NoteStorage {
        id: noteStorage

        onNoteSaved: {
            console.log("note saved!!!");
        }
    }

    GridLayout {
        columns: 2
        rows: 1
        columnSpacing: 0
        anchors.fill: parent

        NoteListView {
            noteStorage: noteStorage
            Layout.preferredWidth: 200
            Layout.fillHeight: true

            onNoteSelected: {
                noteView.note = note;
            }
        }

        NoteView {
            id: noteView
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}

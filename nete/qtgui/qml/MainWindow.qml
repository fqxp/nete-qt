import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.1
import Qt.labs.settings 1.0
import nete 1.0

Window {
    id: window
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

    Settings {
        property alias x: window.x
        property alias y: window.y
        property alias width: window.width
        property alias height: window.height
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

            onNoteCreated: {
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

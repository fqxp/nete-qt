import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.2
import Qt.labs.settings 1.0
import nete 1.0

Window {
    id: window
    width: 640
    height: 400

    FontAwesome {
        id: awesome
    }

    Settings {
        property alias x: window.x
        property alias y: window.y
        property alias width: window.width
        property alias height: window.height
    }

    NoteList {
        id: noteList

        onNoteCreated: {
            noteView.note = note;
            noteView.focusTitleEditor();
        }
    }

    GridLayout {
        columns: 2
        rows: 1
        columnSpacing: 0
        anchors.fill: parent

        NoteListView {
            noteList: noteList
            Layout.preferredWidth: 200
            Layout.fillHeight: true

            onNoteSelected: {
                noteView.note = noteList.note(noteId);
            }
        }

        NoteView {
            id: noteView
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    Action {
        id: quitAction
        shortcut: "Ctrl+q"
        onTriggered: {
            Qt.quit()
        }
    }
}

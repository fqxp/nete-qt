import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2
import Qt.labs.settings 1.0
import nete 1.0

Window {
    id: window
    width: 640
    height: 400
    flags: Qt.Dialog

    property string neteUri
    property var noteList: null

    Component.onCompleted: {
        noteList = NoteListModelFactory.create(neteUri);
    }

    Connections {
        target: noteList
        onNoteCreated: {
            noteView.note = note;
            noteView.focusTitleEditor();
        }
    }

    FontAwesome {
        id: awesome
    }

    Settings {
        property alias x: window.x
        property alias y: window.y
        property alias width: window.width
        property alias height: window.height
    }

    RowLayout {
        spacing: 0
        anchors.fill: parent

        ColumnLayout {
            Layout.maximumWidth: 240

            spacing: 0

            FilterView {
                Layout.fillWidth: true
                noteList: window.noteList
            }

            NoteListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                noteList: window.noteList

                onNoteSelected: {
                    noteView.note = noteList.noteAt(index);
                }
            }
        }

        NoteView {
            id: noteView
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

    Connections {
        target: noteView
        onDeleteNoteRequested: noteList.delete(note)
    }

    Action {
        id: quitAction
        shortcut: "Ctrl+q"
        onTriggered: Qt.quit()
    }
}

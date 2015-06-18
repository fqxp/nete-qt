import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import "controls" as Awesome
import nete 1.0

Rectangle {
    id: container

    property NoteStorage noteStorage
    property var notes: []

    signal noteSelected(var note)
    signal noteCreated(var note)

    Connections {
        id: noteStorageConnections
        target: null

        onNoteListUpdated: {
            container.notes = notes;
            if (container.notes.length > 0) {
                noteSelected(container.notes[0]);
            }
        }
    }

    onNoteStorageChanged: {
        if (noteStorage !== null) {
            noteStorageConnections.target = noteStorage;
            noteStorage.list();
        }
    }

    function createNewNote() {
        var newNote = noteStorage.create();
        var index = notes.add(newNote);
        listView.currentIndex = index;
        noteCreated(newNote);
    }

    Component {
        id: noteDelegate

        Rectangle {
            width: parent.width
            height: 50
            color: ListView.isCurrentItem ? "white" : "#666666"
            border { width: 1; color: "#999999" }

            function select() {
                noteSelected(modelData);
            }

            Text {
                anchors { fill: parent; leftMargin: 10 }
                text: modelData.title
                font { pointSize: 12 }
                color: parent.ListView.isCurrentItem ? "black" : "white"
                elide: Text.ElideRight
                verticalAlignment: Text.AlignVCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (index != parent.ListView.view.currentIndex) {
                        parent.ListView.view.currentIndex = index;
                    }
                }
            }

            Behavior on color {
                ColorAnimation {
                    duration: 100
                    easing.type: Easing.OutCubic
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                id: listView
                anchors.fill: parent
                model: notes
                delegate: noteDelegate

                onCurrentItemChanged: {
                    listView.currentItem.select();
                }
            }
        }

        CreateNoteButton {
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            onClicked: {
                createAction.trigger();
            }
        }
    }

    Action {
        id: createAction
        shortcut: StandardKey.New
        onTriggered: {
            createNewNote();
        }
    }

    Action {
        id: previousNoteAction
        shortcut: "Ctrl+PgUp"
        onTriggered: {
            listView.decrementCurrentIndex();
        }
    }

    Action {
        id: nextNoteAction
        shortcut: "Ctrl+PgDown"
        onTriggered: {
            listView.incrementCurrentIndex();
        }
    }
}

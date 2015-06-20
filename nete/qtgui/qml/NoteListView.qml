import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import nete 1.0

Rectangle {
    id: container

    property NoteList noteList

    signal noteSelected(string noteId)

    Connections {
        id: noteListConnections
        target: null

        onNoteCreated: {
            listView.currentIndex = row;
        }
    }

    onNoteListChanged: {
        noteListConnections.target = noteList;
    }

    Component {
        id: noteDelegate

        Rectangle {
            width: parent.width
            height: 50
            color: ListView.isCurrentItem ? "white" : "#666666"
            border { width: 1; color: "#999999" }

            function select() {
                noteSelected(id);
            }

            Text {
                anchors { fill: parent; leftMargin: 10 }
                text: title
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
                        noteSelected(id);
                    }
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
                model: noteList
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
                createNoteAction.trigger();
            }
        }
    }

    Action {
        id: createNoteAction
        shortcut: StandardKey.New
        onTriggered: {
            noteList.create();
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

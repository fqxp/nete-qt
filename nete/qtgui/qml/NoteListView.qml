import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

Rectangle {
    id: container

    property var noteStorage
    property var notes: []

    signal noteSelected(var note)
    signal noteCreated(var note)

    Connections {
        target: noteStorage
        onNoteListUpdated: {
            container.notes = notes;
            if (container.notes.length > 0) {
                noteSelected(container.notes[0]);
            }
        }
    }

    Component.onCompleted: {
        noteStorage.list();
    }

    Component {
        id: noteDelegate

        Rectangle {
            width: parent.width
            height: 50
            color: ListView.isCurrentItem ? "white" : "#666666"
            border { width: 1; color: "#999999" }

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
                        //wrapper.forceActiveFocus();   // TODO: needed?
                        noteSelected(modelData);
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

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                id: listView
                anchors.fill: parent
                model: notes
                delegate: noteDelegate
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: "#666666"

            Text {
                anchors.fill: parent
                text: "New Note"
                font.pointSize: 16
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    var newNote = noteStorage.create();
                    container.notes = container.notes.concat([newNote])
                    listView.currentIndex = container.notes.length - 1;
                    noteCreated(newNote);
                }
            }
        }
    }
}

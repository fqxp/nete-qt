import QtQuick 2.3
import QtQuick.Controls 1.2

Rectangle {
    id: container

    property var noteStorage
    property var notes: []

    signal noteSelected(var note)

    Connections {
        target: noteStorage
        onNoteListUpdated: {
            container.notes = notes;
        }
    }

    Component.onCompleted: {
        noteStorage.list();
        if (notes.length > 0) {
            noteSelected(notes[0]);
        }
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

    ScrollView {
        anchors.fill: parent

        ListView {
            anchors.fill: parent
            model: notes
            delegate: noteDelegate
        }
    }
}

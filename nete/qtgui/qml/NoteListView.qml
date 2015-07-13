import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import nete 1.0

Rectangle {
    id: container

    property NoteList noteList

    signal noteSelected(int index)

    Connections {
        target: noteList

        onNoteCreated: {
            listView.currentIndex = row;
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
                delegate: NoteListItem {}

                onCurrentItemChanged: {
                    container.noteSelected(listView.currentIndex);
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

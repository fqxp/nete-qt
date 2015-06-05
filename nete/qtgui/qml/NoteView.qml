import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

Rectangle {
    id: container

    property var currentNoteView: emptyNoteView.createObject(this)
    property var note: null

    onNoteChanged: {
        console.log('note changed: ' + container);
        currentNoteView.destroy();
        currentNoteView = ((note !== null)
            ? noteView.createObject(this)
            : emptyNoteView.createObject(this));
    }

    Component {
        id: noteView

        GridLayout {
            columns: 1
            rows: 2
            rowSpacing: 0
            anchors.fill: parent

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: 40

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 3

                    NoteTitleView {
                        note: container.note
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    Button {
                        id: editButton
                        text: "Edit"
                        visible: true
                        Layout.preferredHeight: parent.height - 6
                    }

                    Button {
                        id: doneButton
                        text: "Done"
                        visible: false
                        Layout.preferredHeight: parent.height - 6
                    }
                }
            }

            Rectangle {
                color: 'green'
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    Component {
        id: emptyNoteView

        Text {
            anchors.fill: parent
            text: "No note loaded."
        }
    }
}

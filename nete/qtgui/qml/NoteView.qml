import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

Rectangle {
    id: container

    property Item currentNoteView: emptyNoteView.createObject(this)
    property var note: null

    onNoteChanged: {
        console.log('note changed: ' + container.note);
        currentNoteView.destroy();
        currentNoteView = ((note !== null)
            ? noteView.createObject(this, {note: note})
            : emptyNoteView.createObject(this));
    }

    function focusTitleEditor() {
        currentNoteView.focusTitleEditor();
    }

    Component {
        id: noteView

        GridLayout {
            columns: 1
            rows: 2
            rowSpacing: 0
            anchors.fill: parent

            property var note

            function focusTitleEditor() {
                noteTitleView.state = "editing";
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: 40

                Rectangle {
                    color: "green"
                    anchors.fill: parent
                }

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 3

                    NoteTitleView {
                        id: noteTitleView
                        note: container.note
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    Button {
                        id: editButton
                        text: noteTextView.state == "normal" ? "Edit" : "Done";
                        Layout.preferredHeight: parent.height - 6

                        onClicked: {
                            noteTextView.toggleState();
                        }
                    }
                }
            }

            NoteTextView {
                id: noteTextView
                note: container.note
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
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 16
        }
    }
}

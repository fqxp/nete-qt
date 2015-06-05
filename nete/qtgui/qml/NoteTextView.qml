import QtQuick 2.3
import QtQuick.Controls 1.2
import nete 1.0

Rectangle {
    id: container
    color: "green"
    state: "normal"

    property var note

    function beginEditing() {
        state = "editing";
    }

    function finishEditing() {
        state = "normal";
    }

    function isEditing() {
        return state == "editing";
    }

    states: [
        State {
            name: "normal"
            PropertyChanges { target: noteTextShowView; visible: true }
            PropertyChanges { target: noteTextEditView; visible: false }
        },
        State {
            name: "editing"
            PropertyChanges { target: noteTextEditView; visible: true }
            PropertyChanges { target: noteTextShowView; visible: false }
        }
    ]

    TextArea {
        id: noteTextShowView
        text: MarkdownRenderer.renderToHtml(note.text)
        visible: true
        readOnly: true
        wrapMode: Text.Wrap
        textFormat: TextEdit.RichText
        font { pointSize: 12 }
        anchors.fill: parent
    }

    TextArea {
        id: noteTextEditView
        text: container.note.text
        visible: false
        readOnly: false
        wrapMode: Text.Wrap
        textFormat: TextEdit.PlainText
        font { family: "Courier"; pointSize: 12 }
        anchors.fill: container

        onTextChanged: {
            if (isEditing()) {
                note.text = text;
                note.save();
            }
        }

        Keys.onEscapePressed: {
            container.finishEditing();
        }

        Keys.onReturnPressed: {
            if (event.modifiers == Qt.ControlModifier) {
                container.finishEditing();
            } else {
                event.accepted = false;
            }
        }
    }
}


import QtQuick 2.3
import QtQuick.Controls 1.2
import nete 1.0

Rectangle {
    id: container
    color: "green"
    state: "normal"

    property var note
    property var currentView: null

    function isEditing() {
        return state == "editing";
    }

    function toggleState() {
        state = (state == "normal") ? "editing" : "normal";
    }

    states: [
        State {
            name: "normal"
            StateChangeScript {
                script: {
                    if (currentView !== null) {
                        currentView.destroy();
                    }
                    currentView = noteTextShowView.createObject(container);
                }
            }
        },
        State {
            name: "editing"
            StateChangeScript {
                script: {
                    if (currentView !== null) {
                        currentView.destroy();
                    }
                    currentView = noteTextEditView.createObject(container, {text: container.note.text});
                }
            }
        }
    ]

    Component {
        id: noteTextShowView

        TextArea {
            text: MarkdownRenderer.renderToHtml(note.text)
            readOnly: true
            wrapMode: Text.Wrap
            textFormat: TextEdit.RichText
            font { pointSize: 12 }
            anchors.fill: parent
        }
    }

    Component {
        id: noteTextEditView

        TextArea {
            readOnly: false
            wrapMode: Text.Wrap
            textFormat: TextEdit.PlainText
            font { family: "Courier"; pointSize: 12 }
            anchors.fill: container

            onTextChanged: {
                if (isEditing()) {
                    container.note.text = text;
                    note.save();
                }
            }

            Keys.onEscapePressed: {
                container.state = "normal";
            }
        }
    }

    Action {
        id: editTextAction
        shortcut: "Ctrl+Return"
        onTriggered: {
            toggleState();
        }
    }
}

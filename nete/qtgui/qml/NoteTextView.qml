import QtQuick 2.3
import QtQuick.Controls 1.2
import nete 1.0

Rectangle {
    id: container
    color: "green"
    state: "normal"

    property var note
    property var currentView: null

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
                    note.lazy_save();
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
}


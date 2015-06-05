import QtQuick 2.3
import QtQuick.Layouts 1.1

Item {
    id: container
    state: "normal"

    property var note

    states: [
        State {
            name: "normal"
            PropertyChanges { target: noteTitleEditView; visible: false }
            PropertyChanges { target: noteTitleShowView; visible: true }
        },
        State {
            name: "editing"
            PropertyChanges { target: noteTitleShowView; visible: false }
            PropertyChanges { target: noteTitleEditView; visible: true }
        }
    ]

    NoteTitleShowView {
        id: noteTitleShowView
        title: note.title
        visible: true
        anchors.fill: parent

        onEditRequested: {
            container.state = "editing";
        }
    }

    NoteTitleEditView {
        id: noteTitleEditView
        title: note.title
        visible: false
        anchors.fill: parent

        onEditFinished: {
            note.title = newTitle;
            note.save()
            container.state = "normal";
        }

        onEditCancelled: {
            container.state = "normal";
        }
    }
}

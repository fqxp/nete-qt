import QtQuick 2.3
import QtQuick.Dialogs 1.2

MessageDialog {
    id: dialog
    title: "Really delete note?"
    text: "You really wanna delete the note?"
    icon: StandardIcon.Warning
    standardButtons: StandardButton.Yes | StandardButton.No
    modality: Qt.WindowModal
}

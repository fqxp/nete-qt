import QtQuick 2.3
import QtQuick.Controls 1.2
import nete 1.0

Rectangle {
    height: 40
    color: "red"

    property var noteList

    TextField {
        id: filterExprField
        anchors.fill: parent

        onTextChanged: noteList.setFilter(text)

        Keys.onEscapePressed: {
            text = '';
            focus = false;
        }
    }

    Action {
        id: filterAction
        shortcut: "Ctrl+f"
        onTriggered: filterExprField.focus = true
    }
}

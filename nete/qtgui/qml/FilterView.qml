import QtQuick 2.3
import QtQuick.Controls 1.2
import nete 1.0

Rectangle {
    id: container
    height: 40
    color: "white"
    visible: false

    property var noteList

    onVisibleChanged: {
        if (container.visible) {
            filterExprField.focus = true;
            noteList.setFilter(filterExprField.text);
        } else {
            noteList.setFilter('');
        }
    }

    TextField {
        id: filterExprField
        anchors.fill: parent

        onTextChanged: noteList.setFilter(text)

        Keys.onEscapePressed: {
            text = '';
            focus = false;
        }
    }
}

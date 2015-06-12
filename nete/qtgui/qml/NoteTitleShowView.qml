import QtQuick 2.3

Rectangle {
    color: "transparent"

    property string title

    signal editRequested()

    Text {
        text: title
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 16
        anchors.fill: parent

    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            editRequested();
        }
    }
}

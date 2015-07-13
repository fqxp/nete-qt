import QtQuick 2.3


Rectangle {
    width: parent.width
    height: 50
    color: ListView.isCurrentItem ? "white" : "#666666"
    border { width: 1; color: "#999999" }

    Text {
        anchors { fill: parent; leftMargin: 10 }
        text: title
        font { pointSize: 12 }
        color: parent.ListView.isCurrentItem ? "black" : "white"
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            if (index != parent.ListView.view.currentIndex) {
                parent.ListView.view.currentIndex = index;
            }
        }
    }
}

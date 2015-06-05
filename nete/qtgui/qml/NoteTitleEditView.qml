import QtQuick 2.3
import QtQuick.Controls 1.2

TextField {
    text: title
    font.pointSize: 16

    property string title

    signal editFinished(string newTitle)
    signal editCancelled()

    Keys.onEscapePressed: {
        editCancelled();
    }

    onEditingFinished: {
        editFinished(text);
    }
}


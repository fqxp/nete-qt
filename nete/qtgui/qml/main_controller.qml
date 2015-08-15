import QtQuick 2.0

Item {
    function toggle() {
        mainWindow.visible = !mainWindow.visible;
    }

    MainWindow {
        id: mainWindow
        visible: true
        neteUri: 'nete:notes'
    }
}

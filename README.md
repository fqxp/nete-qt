# Useful Rules

## QML
Do not put any positioning information into top-level components. Makes it
easier to position them from outside.

# Development
Development is organized using a Trello board: https://trello.com/b/YBRdEK7r/nete

# Requirements

Debian packages:

    apt-get install python-pyqt5 python-pyqt5.qtquick python-markdown qml-module-qt-labs-settings qml-module-qtquick2 qml-module-qtquick-window2 qml-module-qtquick-controls qml-module-qtquick-layouts fonts-font-awesome

The current version of PyQt5 shipped with Debian is buggy and nete-qt doesn‘t
work with it. You need to download and install PyQt5 yourself, see http://pyqt.sourceforge.net/Docs/PyQt5/installation.html#downloading-pyqt5
for instructions.

See
http://python.6.x6.nabble.com/Qml-Instantiate-a-model-derived-from-QAbstractListModel-from-qml-td5078937.html
for comments on the bug.

# Credits
* Notepad icon: http://pixabay.com/en/notepad-editor-pencil-document-97841/

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication


class TrayIcon(QSystemTrayIcon):

    def __init__(self,  parent=None):
        super(TrayIcon, self).__init__(parent=parent)
        self.setIcon(QIcon('/home/frank/devel/nete/nete-qt/icons/notepad.png'))
        self.setContextMenu(self.build_menu())
        self.activated.connect(self.on_activated)

    def build_menu(self):
        self.menu = QMenu()

        self.quitAction = QAction('Quit', self.menu)
        self.quitAction.triggered.connect(self.on_quit_requested)
        self.menu.addAction(self.quitAction)

        return self.menu

    def on_quit_requested(self):
        QApplication.quit()

    def on_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.parent().toggle()

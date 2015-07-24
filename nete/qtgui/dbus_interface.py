from PyQt5.QtCore import pyqtSlot, Q_CLASSINFO
from PyQt5.QtDBus import QDBusAbstractAdaptor


class MainControllerAdaptor(QDBusAbstractAdaptor):

    Q_CLASSINFO("D-Bus Interface", 'de.fqxp.nete.MainController')

    Q_CLASSINFO("D-Bus Introspection", ''
        '  <interface name="de.fqxp.nete.MainController">\n'
        '    <method name="toggle"/>\n'
        '  </interface>\n'
        '')

    def __init__(self, parent):
        super(MainControllerAdaptor, self).__init__(parent)

        self.setAutoRelaySignals(True)

    @pyqtSlot()
    def toggle(self):
        self.parent().toggle()


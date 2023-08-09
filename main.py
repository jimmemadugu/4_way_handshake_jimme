from PySide6.QtWidgets import QApplication
#from handshakeWidget import HandshakeWidget
from tabWidget import TabWidget

app = QApplication()

window = TabWidget()
window.show()

app.exec()
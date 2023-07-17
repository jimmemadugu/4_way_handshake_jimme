from PySide6.QtWidgets import QApplication
from handshakeWidget import HandshakeWidget

app = QApplication()

window = HandshakeWidget()
window.show()

app.exec()
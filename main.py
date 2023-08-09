from PySide6.QtWidgets import QApplication, QTextBrowser
#from handshakeWidget import HandshakeWidget
from tabWidget import TabWidget

app = QApplication()
textBrowser = QTextBrowser()

window = TabWidget(textBrowser)
window.show()

app.exec()
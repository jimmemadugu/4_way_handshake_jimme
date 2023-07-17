from PySide6.QtWidgets import QMainWindow

# main window class for 4 way handshake widget
class HandshakeWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4 Way Handshake Simulator")
        
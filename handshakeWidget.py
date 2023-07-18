from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout

# main window class for 4 way handshake widget
class HandshakeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4 Way Handshake Simulator")

        btnRegularHandshake = QPushButton("Regular Handshake Protocol")
        btnRegularHandshake.clicked.connect(self.simulateRegularHandshake)

        btnModifiedHandshake = QPushButton("Modified Handshake Protocol")
        btnModifiedHandshake.clicked.connect(self.simulateModifiedHandshake)

        #Horizontal arrangement
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(btnRegularHandshake)
        widgetLayout.addWidget(btnModifiedHandshake)

        self.setLayout(widgetLayout)
    
    # slot for Regular Handshake Button
    def simulateRegularHandshake(self):
        print("Begin Regular Handshake Protocol Simulation")

    # slot for Modified Handshake Button
    def simulateModifiedHandshake(self):
        print("Begin Modified Handshake Protocol Simulation")
        
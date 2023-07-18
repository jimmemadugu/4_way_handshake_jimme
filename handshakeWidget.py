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

        btnRegularHandshakeBatch = QPushButton("Regular Handshake Protocol Batch")
        #btnRegularHandshakeBatch.clicked.connect(self.simulateRegularHandshakeBatch)

        btnModifiedHandshakeBatch = QPushButton("Modified Handshake Protocol Batch")
        #btnModifiedHandshakeBatch.clicked.connect(self.simulateModifiedHandshakeBatch)

        #Horizontal arrangement for btnRegularHandshake and btnModifiedHandshake buttons
        # widgetLayout = QHBoxLayout()
        # widgetLayout.addWidget(btnRegularHandshake)
        # widgetLayout.addWidget(btnModifiedHandshake)

        # #Horizontal arrangement for simulateRegularHandshakeBatch and simulateModifiedHandshakeBatch buttons
        # widgetLayout2 = QHBoxLayout()
        # widgetLayout2.addWidget(btnRegularHandshakeBatch)
        # widgetLayout2.addWidget(btnModifiedHandshakeBatch)

        widgetVLayout = QVBoxLayout()
        widgetVLayout.addWidget(btnRegularHandshake)
        widgetVLayout.addWidget(btnModifiedHandshake)
        widgetVLayout.addWidget(btnRegularHandshakeBatch)
        widgetVLayout.addWidget(btnModifiedHandshakeBatch)

        self.setLayout(widgetVLayout)
    
    # slot for Regular Handshake Button
    def simulateRegularHandshake(self):
        print("Begin Regular Handshake Protocol Simulation")

    # slot for Modified Handshake Button
    def simulateModifiedHandshake(self):
        print("Begin Modified Handshake Protocol Simulation")
        
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit, QSpacerItem, QTextBrowser
from PySide6.QtCore import QTimer
from suplicantProcesses import SuplicantProcesses

class TabWidget(QWidget):
    

    def __init__(self, textBrowser):
        super().__init__()
       
        self.setWindowTitle("4-Way Handshake Simulation")
        self.textBrowser = textBrowser
        self.is_button_enabled = True
        self.is_socket_operation_ongoing = False

        # timer object
        self.timer = QTimer()
        self.timer.timeout.connect(self.enable_buttons)

        tab_widget = QTabWidget(self)
        #textBrowser = QTextBrowser()
        self.textBrowser.setText("Started 4-Way Handshake Simulation...\n")

        # Single Simulation
        widget_single_simulation = QWidget()
        self.btnRegularHandshake = QPushButton("Regular Handshake Protocol")
        self.btnRegularHandshake.clicked.connect(self.simulateRegularHandshake)

        self.btnModifiedHandshake = QPushButton("Modified Handshake Protocol")
        self.btnModifiedHandshake.clicked.connect(self.simulateModifiedHandshake)

        single_simulation_layout = QHBoxLayout()
        single_simulation_layout.addWidget(self.btnRegularHandshake)
        single_simulation_layout.addWidget(self.btnModifiedHandshake)

        single_simulation_v_layout = QVBoxLayout()
        single_simulation_v_layout.addLayout(single_simulation_layout)
        single_simulation_v_layout.addWidget(textBrowser)

        widget_single_simulation.setLayout(single_simulation_v_layout)

        # Batch Simulation
        widget_batch__simulation = QWidget()
        btnRegularHandshakeBatch = QPushButton("Regular Handshake Protocol Batch")
        btnRegularHandshakeBatch.clicked.connect(self.simulateRegularHandshakeBatch)

        btnModifiedHandshakeBatch = QPushButton("Modified Handshake Protocol Batch")
        btnModifiedHandshakeBatch.clicked.connect(self.simulateModifiedHandshakeBatch)

        batch_file_upload_widget = QLineEdit()

        batch_simulation_layout = QHBoxLayout()
        batch_simulation_layout.addWidget(btnRegularHandshakeBatch)
        batch_simulation_layout.addWidget(btnModifiedHandshakeBatch)

        batch_simulation_v_layout = QVBoxLayout()
        batch_simulation_v_layout.addWidget(batch_file_upload_widget)
        batch_simulation_v_layout.addLayout(batch_simulation_layout)

        widget_batch__simulation.setLayout(batch_simulation_v_layout)

        #Add tabs to widget
        tab_widget.addTab(widget_single_simulation,"Single")
        tab_widget.addTab(widget_batch__simulation,"Batch")

        layout = QVBoxLayout()
        layout.addWidget(tab_widget)

        self.setLayout(layout)

    
    # slot for Regular Handshake Button
    def simulateRegularHandshake(self):
        print("Begin Regular Handshake Protocol Simulation")


    # slot for Modified Handshake Button
    def simulateModifiedHandshake(self):
        print("Begin Modified Handshake Protocol Simulation")
        sup = SuplicantProcesses()

        # Disable UI Buttons
        self.is_button_enabled = False
        self.btnModifiedHandshake.setEnabled(self.is_button_enabled)
        self.btnRegularHandshake.setEnabled(self.is_button_enabled)

        # Set delay for socket operations to finsh
        self.timer.start(3000)
        self.is_socket_operation_ongoing = True
        # self.run_supli


        # Display Parameters
        print(sup.returnParametersString())
        self.textBrowser.append(sup.returnParametersString())

        # message
        self.textBrowser.append("Socket operation has started\n")
        

    # slot for Regular Handshake Batch Button
    def simulateRegularHandshakeBatch(self):
        print("Begin Batch Regular Handshake Protocol Simulation")


    # slot for Modified Handshake Batch Button
    def simulateModifiedHandshakeBatch(self):
        print("Begin Batch Modified Handshake Protocol Simulation")

    def enable_buttons(self):
        self.is_button_enabled = True
        self.is_socket_operation_ongoing = False

        self.btnRegularHandshake.setEnabled(self.is_button_enabled)
        self.btnModifiedHandshake.setEnabled(self.is_button_enabled)
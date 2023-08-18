from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit, QSpacerItem, QTextBrowser
from PySide6.QtCore import QTimer, QRunnable, Slot, QThreadPool
from suplicantProcesses import SuplicantProcesses
from authenticatorProcesses import AuthenticatorProcesses
import time

class TabWidget(QWidget):
    

    def __init__(self, textBrowser):
        super().__init__()
       
        self.setWindowTitle("4-Way Handshake Simulation")
        self.textBrowser = textBrowser
        self.is_button_enabled = True
        self.is_socket_operation_ongoing = False

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # timer object
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.enable_buttons)

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

        #labels
        self.labelSuplicant = QLabel("Supplicant")
        self.labelAttacker = QLabel("Attacker")
        self.labelAuthenticator = QLabel("Authenticator")
        #labels' layout
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.labelSuplicant)
        label_layout.addWidget(self.labelAttacker)
        label_layout.addWidget(self.labelAuthenticator)

        #textBrowser
        self.textBrowserSuplicant = QTextBrowser()
        self.textBrowserAttacker = QTextBrowser()
        self.textBrowserAuthenticator = QTextBrowser()
        #textBrowsers' layout
        text_browser_layout = QHBoxLayout()
        text_browser_layout.addWidget(self.textBrowserSuplicant)
        text_browser_layout.addWidget(self.textBrowserAttacker)
        text_browser_layout.addWidget(self.textBrowserAuthenticator)

        
        # Suplicant Processes instance
        self.sup = SuplicantProcesses(self.textBrowserSuplicant)

        # Authenticator instance
        self.aut = AuthenticatorProcesses(self.textBrowserAuthenticator)

        #PushButtons
        btnStartSuplicant = QPushButton("Start Suplicant")
        btnStartSuplicant.clicked.connect(self.startSuplicant)

        btnStartAttacker = QPushButton("Start Attacker")
        #btnStartAttacker.clicked.connect(self.startAttacker)

        btnStartAuthenticator = QPushButton("Start Authenticator")
        btnStartAuthenticator.clicked.connect(self.startAuthenticator)

        #PushButtons' Layout
        push_button_layout = QHBoxLayout()
        push_button_layout.addWidget(btnStartSuplicant)
        push_button_layout.addWidget(btnStartAttacker)
        push_button_layout.addWidget(btnStartAuthenticator)

        single_simulation_v_layout = QVBoxLayout()
        single_simulation_v_layout.addLayout(single_simulation_layout)
        single_simulation_v_layout.addWidget(textBrowser)
        single_simulation_v_layout.addLayout(label_layout)
        single_simulation_v_layout.addLayout(text_browser_layout)
        single_simulation_v_layout.addLayout(push_button_layout)

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
        # Suplicant Processes instance
        # sup = SuplicantProcesses()

        self.sup.initializeParameters()

        # Disable UI Buttons
        self.is_button_enabled = False
        self.btnModifiedHandshake.setEnabled(self.is_button_enabled)
        self.btnRegularHandshake.setEnabled(self.is_button_enabled)

        # Display Parameters
        print(self.sup.returnParametersString())
        self.textBrowser.append(self.sup.returnParametersString())

        # message
        # self.textBrowser.append("Socket operation has started\n")

        # Set delay for socket operations to finsh
        #self.timer.start(15000)
        # self.is_socket_operation_ongoing = True
        # try:
        #     # start supplicant
        #sup.run()
        # self.threadpool.start(self.sup)

        #     # sup.runSupplicantProcesses(self.textBrowser, 8080)
            
        #     # Authenticator Processes instance
        #     #aut = AuthenticatorProcesses()
        #     # start authenticator
        #     #aut.run(self.textBrowser)
        # except Exception as e:
        #     print(f"Exception occured: {str(e)}")

    # slot for Regular Handshake Batch Button
    def simulateRegularHandshakeBatch(self):
        print("Begin Batch Regular Handshake Protocol Simulation")


    # slot for Modified Handshake Batch Button
    def simulateModifiedHandshakeBatch(self):
        print("Begin Batch Modified Handshake Protocol Simulation")

    # # Socket functions
    # def runSupplicantProcesses(self, port=8080):
    #     self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     self.server_socket.bind((socket.gethostname(),8080))
    #     self.server_socket.listen(5)
    #     self.sockets_list = [self.server_socket]
    #     print("Client started. Waiting for connections...")

    #     return 
    
    # def listenForReadSockets():
    #     while is_running:
    #     print("Client started. Waiting for connections...")
    #     self.read_sockets, _, _ = select.select(self.sockets_list, [], [])

    def startSuplicant(self):
        self.threadpool.start(self.sup)
    
    def startAuthenticator(self):
        self.threadpool.start(self.aut)

    def enable_buttons(self):
        self.is_button_enabled = True
        self.is_socket_operation_ongoing = False

        self.btnRegularHandshake.setEnabled(self.is_button_enabled)
        self.btnModifiedHandshake.setEnabled(self.is_button_enabled)
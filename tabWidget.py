from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit,QSpacerItem

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
       
        self.setWindowTitle("4-Way Handshake Simulation")

        tab_widget = QTabWidget(self)

        # Single Simulation
        widget_single_simulation = QWidget()
        btnRegularHandshake = QPushButton("Regular Handshake Protocol")
        btnRegularHandshake.clicked.connect(self.simulateRegularHandshake)

        btnModifiedHandshake = QPushButton("Modified Handshake Protocol")
        btnModifiedHandshake.clicked.connect(self.simulateModifiedHandshake)
        single_simulation_layout = QHBoxLayout()
        single_simulation_layout.addWidget(btnRegularHandshake)
        single_simulation_layout.addWidget(btnModifiedHandshake)
        widget_single_simulation.setLayout(single_simulation_layout)

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

        #Information
        # widget_form = QWidget()
        # label_full_name = QLabel("Full name :")
        # line_edit_full_name = QLineEdit()
        # form_layout = QHBoxLayout()
        # form_layout.addWidget(label_full_name)
        # form_layout.addWidget(line_edit_full_name)
        # widget_form.setLayout(form_layout)

        #Buttons
        # widget_buttons = QWidget()
        # button_1 = QPushButton("One")
        # button_1.clicked.connect(self.button_1_clicked)
        # button_2 = QPushButton("Two")
        # button_3 = QPushButton("Three")
        # buttons_layout = QVBoxLayout()
        # buttons_layout.addWidget(button_1)
        # buttons_layout.addWidget(button_2)
        # buttons_layout.addWidget(button_3)
        # widget_buttons.setLayout(buttons_layout)


        #Add tabs to widget
        tab_widget.addTab(widget_single_simulation,"Single")
        tab_widget.addTab(widget_batch__simulation,"Batch")


        layout = QVBoxLayout()
        layout.addWidget(tab_widget)

        self.setLayout(layout)

    def button_1_clicked(self):
        print("Button clicked")
    
    # slot for Regular Handshake Button
    def simulateRegularHandshake(self):
        print("Begin Regular Handshake Protocol Simulation")

    # slot for Modified Handshake Button
    def simulateModifiedHandshake(self):
        print("Begin Modified Handshake Protocol Simulation")

    # slot for Regular Handshake Batch Button
    def simulateRegularHandshakeBatch(self):
        print("Begin Batch Regular Handshake Protocol Simulation")

    # slot for Modified Handshake Batch Button
    def simulateModifiedHandshakeBatch(self):
        print("Begin Batch Modified Handshake Protocol Simulation")
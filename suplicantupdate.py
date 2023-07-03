import time
from threading import*
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import hmac
import hashlib
import os
import socket
import pickle
import select
from PyQt5.uic import loadUiType
ui,_=loadUiType('server.ui')
class MainApp(QMainWindow,ui):
        def __init__(self):
                QMainWindow.__init__(self)
                self.setupUi(self)
                self.displayparameters()
                self.pushButton_supplicant.clicked.connect(self.supplicants)
        def supplicants(self):
                self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server_socket.bind((socket.gethostname(),8080))
                self.server_socket.listen(5)
                self.sockets_list = [self.server_socket]
                #self.textBrowser_2.append("Client started. Waiting for connections...")
                while True:
                        print("Client started. Waiting for connections...")
                        self.read_sockets, _, _ = select.select(self.sockets_list, [], [])
                        for self.sock in self.read_sockets:
                                # New connection received
                                if self.sock == self.server_socket:
                                        self.client_socket, self.client_address = self.server_socket.accept()
                                        self.sockets_list.append(self.client_socket)
                                        print(f"New connection from {self.client_address}")
                                        
                                       
                                        
                                # Existing client sending a message
                                else:
                                        self.data = self.sock.recv(1024)
                                        if self.data:
                                                self.dic1=pickle.loads(self.data)
                                                self.apnonce=self.dic1.get('apnonce')
                                                self.apmac=self.dic1.get('apmac')
                                                self.channel=self.dic1.get('channelinfo')
                                                self.beta=self.dic1.get('β')
                                                self.ptk=(self.spNonce().hex()+self.clientMacAddress()+self.apmac.hex()+self.apnonce.hex()+self.generate_pmk().hex())
                                                self.PTK=self.ptk[0:96]
                                                print("Supplicant Pairwise Transient key (PTK):"+self.PTK)
                                                print('Key Confirmation Key (KCK):'+self.PTK[0:32])
                                                print('Key Encryption Key (KEK):'+self.PTK[32:64])
                                                print('Temporal Key (TK):'+self.PTK[64:96])
                                                print(f"Received data from {self.sock.getpeername()}: {self.dic1}")
                                                self.dic2={'spnonce':os.urandom(32),'smac':b'\x77\x88\x99\xaa\xbb\xcc','channelinfo':1}
                                                self.message2=pickle.dumps(self.dic2)
                                                self.sock.send(self.message2)
                                                print('message2 sent sucessfully')
                                                if ((self.beta==True) & (self.channel==1)):
                                                        self.bytedic4=self.sock.recv(1024)
                                                        self.dic5=pickle.loads(self.bytedic4)
                                                        self.GTK=self.dic5.get('gtk')
                                                        print('Install PTK and GTK')
                                                        print('message3 received')
                                                        print('Group Temporal key is:'+self.GTK[0:32].hex())
                                                        print(str(self.beta))
                                                else:
                                                        self.msg='message discarded, use the appropriate channel information'
                                                        self.sock.send(self.msg.encode())

                                                self.beta=False
                                                self.message4='Acknowledge reception of message3, PTK and GTK successfully installed by the supplicant'
                                                self.sock.send(self.message4.encode())
                                                print('Four way handshake completed')
                                                print(str(self.beta))
                                        else:
                                                # Client disconnected
                                                print(f"Client {self.sock.getpeername()} disconnected")
                                                self.sockets_list.remove(self.sock)
                                                self.sock.close()
                                
        def displayparameters(self):
                        self.spnonce=self.spNonce()
                        self.amac= self.apMacAddress()
                        self.smac=self.clientMacAddress()
                        self.textBrowser.setText("supplicants parameters...")
                        self.textBrowser.append("SPs Nonce="+str(self.spnonce.hex()))
                        self.textBrowser.append("supplicants Mac address="+self.smac)
                        self.textBrowser.append("APs Mac address="+self.amac)
                        self.pmk=self.generate_pmk()
                        self.textBrowser.append("supplicants pmk="+str(self.pmk.hex()))
        def spNonce(self):
                        self.snonce = os.urandom(32)
                        return self.snonce
        def clientMacAddress(self):
                self.spa= b"\x77\x88\x99\xaa\xbb\xcc"
                return self.spa.hex()
        def apMacAddress(self):
                        self.aa = b"\x11\x22\x33\x44\x55\x66"
                        return self.aa.hex()
        def generate_pmk(self):
                self.password = "secret_password"
                self.ssid = "example_network"
                return hashlib.pbkdf2_hmac('sha1', self.password.encode(), self.ssid.encode(), 4096, 32)

def main():
        app=QApplication(sys.argv)
        window=MainApp()
        window.show()
        sys.exit(app.exec_())
if __name__ == '__main__':
        main()
        

import sys
# import hmac
import asyncio
import hashlib
import os
import pickle
import select
import socket
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRunnable, Slot

import time

# Constants for Sockect Connection
HOST = "127.0.0.1"
PORT = 8080

class SuplicantProcesses(QRunnable):
    def __init__(self, textBrowser):
        super(SuplicantProcesses, self).__init__()
        self.textBrowser = textBrowser
        print("created new supplicant object processes")
        self.textBrowser.append("created new supplicant object processes")
        self.initializeParameters()
    
    def initializeParameters(self):
        print("displaying supplicant object parameters")
        self.spnonce=self.spNonce()
        self.amac= self.apMacAddress()
        self.smac=self.clientMacAddress()
        self.pmk=self.generate_pmk()

    def returnParametersString(self):
        self.textBrowser.append("supplicants parameters...")
        # time.sleep(2)
        self.textBrowser.append("SPs Nonce="+str(self.spnonce.hex()))
        # time.sleep(1)
        self.textBrowser.append("supplicants Mac address="+self.smac)
        # time.sleep(3)
        self.textBrowser.append("APs Mac address="+self.amac)
        # time.sleep(1)
        self.textBrowser.append("supplicants pmk="+str(self.pmk.hex()))

        return  (
            "supplicants parameters..." + "\n"
            "SPs Nonce="+str(self.spnonce.hex()) + "\n"
            "supplicants Mac address="+self.smac + "\n"
            "APs Mac address="+self.amac + "\n"
            "supplicants pmk="+str(self.pmk.hex()) + "\n"
        )
    
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
    
    async def handle_suplicant_communication(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        data = None

        while data != b"quit":

            try:
                # Receive messages from Authenticator          
                data = await reader.read(1024)
                self.dic1 = pickle.loads(data)
                print("msg ::  ")
                print(self.dic1)
                addr, port = writer.get_extra_info("peername")
                print(f"Message from device with address {addr}:{port}")
                self.textBrowser.append(f"Message from device with address {addr}:{port}")

                # Receive message 1 from Authenticator
                if (self.dic1.get('msg_no') == 1):
                    self.apnonce = self.dic1.get('apnonce')
                    self.apmac=self.dic1.get('apmac')
                    self.channel=self.dic1.get('channelinfo')
                    self.beta=self.dic1.get('β')
                    self.ptk=(self.spNonce().hex()+self.clientMacAddress()+self.apmac.hex()+self.apnonce.hex()+self.generate_pmk().hex())
                    self.PTK=self.ptk[0:96]

                    print("Supplicant Pairwise Transient key (PTK):"+self.PTK)
                    print('Key Confirmation Key (KCK):'+self.PTK[0:32])
                    print('Key Encryption Key (KEK):'+self.PTK[32:64])
                    print('Temporal Key (TK):'+self.PTK[64:96])
                    self.textBrowser.append(f"Supplicant Pairwise Transient key (PTK): {self.PTK}")
                    self.textBrowser.append(f"Key Confirmation Key (KCK): {self.PTK[0:32]}")
                    self.textBrowser.append(f"Key Encryption Key (KEK): {self.PTK[32:64]}")
                    self.textBrowser.append(f"Temporal Key (TK): {self.PTK[64:96]}")
                    
                    await asyncio.sleep(1)
                    # Send second message to Authenticator
                    self.dic2 = {'msg_no':2,'spnonce':os.urandom(32),'smac':b'\x77\x88\x99\xaa\xbb\xcc','channelinfo':1}
                    self.message2 = pickle.dumps(self.dic2)
                    # # self.sock.send(self.message2)
                    print(self.message2)
                    writer.write(self.message2)
                    await writer.drain()
                    self.textBrowser.append("message 2 sent sucessfully")
                    print('message 2 sent sucessfully')

                    await asyncio.sleep(1)
                elif (self.dic1.get('msg_no') == 3):
                    print("Received message three")
                    print(self.dic1)
                    # await asyncio.sleep(2)
                    print(f"beta: {self.beta}")
                    print(f"Channel: {self.channel}")

                    if ((self.beta == True) & (self.channel == 1)):
                        # self.bytedic4=self.sock.recv(1024)
                        # self.bytedic4 = await reader.read(1024)
                        # self.dic5 = pickle.loads(self.bytedic4)

                        self.GTK = self.dic1.get('gtk')
                        print('Install PTK and GTK')
                        print('message3 received')
                        print('Group Temporal key is:'+self.GTK[0:32].hex())

                        self.textBrowser.append('message3 received')
                        self.textBrowser.append('Install PTK and GTK')
                        self.textBrowser.append(f'Group Temporal key is: {self.GTK[0:32].hex()}')

                        self.beta = False
                        self.message4='Acknowledge reception of message3, PTK and GTK successfully installed by the supplicant'
                        # self.sock.send(self.message4.encode())
                        self.dic4 = {'msg_no':4, 'msg':self.message4}
                        self.message = pickle.dumps(self.dic4)
                        print(f"final message : {self.message}")
                        writer.write(self.message)
                        await writer.drain()
                        # await asyncio.sleep(3)
                        print('Four way handshake completed')
                        self.textBrowser.append('Four way handshake completed')

                    else:
                        self.msg='message discarded, use the appropriate channel information'
                        # self.sock.send(self.msg.encode())
                        self.dic2 = {'msg_no':5, 'msg':self.msg}
                        self.message = pickle.dumps(self.dic2)
                        print(f"Error message : {self.message}")
                        writer.write(self.message)
                        await writer.drain()

                    
                    

            except Exception as e:
                print("Exception was raised")
                print("Exited System")
                print(f"An exception occurred: {str(e)}")
            
            
            # msg = data.decode()

            # addr, port = writer.get_extra_info("peername")
            # print(f"Message from {addr}:{port}: {msg!r}")
            # self.textBrowser.append(f"Message from {addr}:{port}: {msg!r}")

            writer.write(data)
            await writer.drain()
        
        print("clossing server")
        self.textBrowser.append("clossing server")
        writer.close()
        await writer.wait_closed()
        print("clossed server")
        self.textBrowser.append("clossed server")

        #raise SystemExit
        raise KeyboardInterrupt 
        #raise Exception('Closing server Exception')

    async def run_server(self) -> None:
        try:
            print("start server")
            self.textBrowser.append("start server")
            server = await asyncio.start_server(self.handle_suplicant_communication, HOST, PORT)
            print("***start server***")
            self.textBrowser.append("***start server***")
            async with server:
                await server.serve_forever()
                print("end server")
                self.textBrowser.append("end server")
            
            print("***end of server operation***")
            self.textBrowser.append("***end of server operation***")
        except Exception as e:
            print("Exception was raised")
            print("Exited System")
            print(f"An exception occurred: {str(e)}")

    @Slot()
    def run(self):
        print("beginning of supplicant program")
        self.textBrowser.append("beginning of supplicant program")

        asyncio.run(self.run_server())
        # time.sleep(10)
        print("end of supplicant program")
        self.textBrowser.append("end of supplicant program")


    # Socket functions
    def runSupplicantProcesses(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostname(),PORT))
        self.server_socket.listen(5)
        self.sockets_list = [self.server_socket]
        print("Supplicant has started")
        # textBrowser.append("Supplicant has started\n")

        is_running = True
        while is_running:
            print("Supplicant is waiting for authenticator...")
            # textBrowser.append("Supplicant is waiting for authenticator...\n")
            self.read_sockets, _, _ = select.select(self.sockets_list, [], [])

            for self.sock in self.read_sockets:
                # New connection received
                if self.sock == self.server_socket:
                    self.client_socket, self.client_address = self.server_socket.accept()
                    self.sockets_list.append(self.client_socket)
                    print(f"New connection from {self.client_address}")
                    # textBrowser.append(f"New connection from {self.client_address}\n")        
                        
                # Existing client sending a message
                else:
                    self.data = self.sock.recv(1024)
                    if self.data:
                        self.dic1 = pickle.loads(self.data)
                        self.apnonce = self.dic1.get('apnonce')
                        self.apmac = self.dic1.get('apmac')
                        self.channel = self.dic1.get('channelinfo')
                        self.beta = self.dic1.get('β')
                        self.ptk = (self.spNonce().hex()+self.clientMacAddress()+self.apmac.hex()+self.apnonce.hex()+self.generate_pmk().hex())
                        self.PTK = self.ptk[0:96]

                        print("Supplicant Pairwise Transient key (PTK):"+self.PTK)
                        print('Key Confirmation Key (KCK):'+self.PTK[0:32])
                        print('Key Encryption Key (KEK):'+self.PTK[32:64])
                        print('Temporal Key (TK):'+self.PTK[64:96])
                        print(f"Received data from {self.sock.getpeername()}: {self.dic1}")

                        # textBrowser.append("Supplicant Pairwise Transient key (PTK):"+self.PTK + '\n')
                        # textBrowser.append('Key Confirmation Key (KCK):'+self.PTK[0:32] + '\n')
                        # textBrowser.append('Key Encryption Key (KEK):'+self.PTK[32:64] + '\n')
                        # textBrowser.append('Temporal Key (TK):'+self.PTK[64:96] + '\n')
                        # textBrowser.append(f"Received data from {self.sock.getpeername()}: {self.dic1}\n")
                        
                        self.dic2 = {'spnonce':os.urandom(32),'smac':b'\x77\x88\x99\xaa\xbb\xcc','channelinfo':1}
                        self.message2 = pickle.dumps(self.dic2)
                        self.sock.send(self.message2)
                        print('message2 sent sucessfully')
                        # textBrowser.append("message2 sent sucessfully\n")
                        
                        if ((self.beta == True) & (self.channel == 1)):
                            self.bytedic4 = self.sock.recv(1024)
                            self.dic5 = pickle.loads(self.bytedic4)
                            self.GTK = self.dic5.get('gtk')
                            print('Install PTK and GTK')
                            print('message3 received')
                            print('Group Temporal key is:'+self.GTK[0:32].hex())
                            print(str(self.beta))

                            # textBrowser.append('Install PTK and GTK\n')
                            # textBrowser.append('message3 received\n')
                            # textBrowser.append('Group Temporal key is:'+self.GTK[0:32].hex() + '\n')
                            # textBrowser.append(str(self.beta) + '\n')
                        else:
                            self.msg = 'message discarded, use the appropriate channel information'
                            self.sock.send(self.msg.encode())

                        self.beta = False
                        self.message4 = 'Acknowledge reception of message3, PTK and GTK successfully installed by the supplicant'
                        self.sock.send(self.message4.encode())

                        print('Four way handshake completed')
                        print(str(self.beta))

                        # textBrowser.append('Four way handshake completed\n')
                        # textBrowser.append(str(self.beta) + '\n')
                    else:
                        # Client disconnected
                        print(f"Client {self.sock.getpeername()} disconnected")

                        # textBrowser.append(f"Client {self.sock.getpeername()} disconnected\n")
                        self.sockets_list.remove(self.sock)
                        self.sock.close()
                        # textBrowser.append("closed supplicant socket\n")
                        is_running = False




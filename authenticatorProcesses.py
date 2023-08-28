import asyncio
import os
import pickle
import time
import hashlib

from PySide6.QtCore import QRunnable, Slot

# Constants for Sockect Connection
HOST = "127.0.0.1"
PORT = 8080

class AuthenticatorProcesses(QRunnable):
    def __init__(self, textBrowser):
        super(AuthenticatorProcesses, self).__init__()
        self.counter = 0
        self.allow_communication = False
        self.waiting_for_message = False
        self.textBrowser = textBrowser
        print("created new authenticator object processes")
        self.textBrowser.append("created new authenticator object processes")
        #self.initializeParameters()
    
    def initializeParameters(self):
        self.apnonce = self.apNonce()
        self.amac = self.apMacAddress()
        self.smac = self.clientMacAddress()
        self.textBrowser.setText("Initializing Authenticators parameters...")
        self.textBrowser.append(f"APs Nonce = {str(self.apnonce.hex())}")
        self.textBrowser.append(f"supplicants Mac address = {self.smac}")
        self.textBrowser.append(f"APs Mac address = {self.amac}")
        self.pmk = self.generate_pmk()
        self.textBrowser.append(f"APs pmk = {str(self.pmk.hex())}")


    def apNonce(self):
        self.anonce = os.urandom(32)
        return self.anonce


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

    
    async def run_client(self) -> None:
        reader, writer = await asyncio.open_connection(HOST, PORT)

        self.counter +=1
        print(f"run client counter: {self.counter}")

        while True:            
            # when authenticator waits for a message from suplicant
            if (self.waiting_for_message):
                # Receive message from Suplicant
                data = await reader.read(1024)
                # await asyncio.sleep(5)
                print("Data from server is :")
                # print(data)
                # print(data.decode())
                # print(type(data))
                self.dic2 = pickle.loads(data)
                print(self.dic2)

                if (self.dic2.get('msg_no') == 2):
                    print("inside message no 2")
                    print("msg ::  ")
                    print(self.dic2)
                    self.spnonce = self.dic2.get('spnonce')
                    self.spmac = self.dic2.get('smac')
                    #print('supplicants nonce:'+str(self.spnonce))
                    #print('supplicants mac address:'+str(self.spmac))
                    self.PTK = (self.generate_pmk().hex()+self.spnonce.hex()+self.spmac.hex()+self.apMacAddress()+self.apNonce().hex())
                    self.textBrowser.append('Authenticators PTK:'+self.PTK[0:96])
                    self.textBrowser.append('Key Confirmation Key (KCK):'+self.PTK[0:32])
                    self.textBrowser.append('Key Encryption Key (KEK):'+self.PTK[32:64])
                    self.textBrowser.append('Temporal Key (TK):'+self.PTK[64:96])
                    self.gtk = os.urandom(32)
                    # Sending message 3 from authenticator to suplicant
                    print("prepare to send message 3")
                    self.dic3 = {'msg_no':3, 'gtk':self.gtk, 'channelinfo':1, 'apmac':b'\x11\x22\x33\x44\x55\x66', 'apnonce':os.urandom(32)}
                    self.message3 = pickle.dumps(self.dic3)
                    writer.write(self.message3)
                    await writer.drain()
                    self.textBrowser.append('message 3 sent successfully')
                    self.textBrowser.append(f"The group Temporal key is: {self.gtk[0:32].hex()}")
                    await asyncio.sleep(1)

                    # self.waiting_for_message = False

                elif (self.dic2.get('msg_no') == 4):
                    print("inside message no 4")
                    self.textBrowser.append(self.dic2.get('msg'))
                    self.textBrowser.append('Four way Handshake completed, PTK installed on the authenticator')
                    self.allow_communication = True
                    print('Four way Handshake completed, PTK installed on the authenticator')
                    await asyncio.sleep(6)
                    writer.write(b"quit")
                    await writer.drain()
                elif (self.dic2.get('msg_no') == 5):
                    print("inside message no 5")
                    self.textBrowser.append(self.dic2.get('msg'))
                    self.allow_communication = False
                    print('***ERROR***')
                    
                    await asyncio.sleep(6)
                    writer.write(b"quit")
                    await writer.drain()
                    writer.close()
                    break
            else:
                # sending message 1 to suplicant
                self.dic = {'msg_no':1,'apnonce':os.urandom(32),'β':True,'channelinfo':1,'apmac':b'\x11\x22\x33\x44\x55\x66'}
                self.message1 = pickle.dumps(self.dic)
                print((self.dic))
                # print(type(self.message1))
                # send message 1 to suplicant
                writer.write(self.message1)
                await writer.drain()
                self.textBrowser.append("message 1 sent successfully")
                self.waiting_for_message = True
                # sleep for 1 second
                await asyncio.sleep(1)


    @Slot()
    def run(self):
        print("beginning of Authenticator program")
        self.textBrowser.append("beginning of Authenticator program")
        asyncio.run(self.run_client())
        print("end of authenticator program")
        self.textBrowser.append("end of authenticator program")
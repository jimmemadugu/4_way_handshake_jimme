import asyncio
import os
import pickle
import time

from PySide6.QtCore import QRunnable, Slot

# Constants for Sockect Connection
HOST = "127.0.0.1"
PORT = 8080

class AuthenticatorProcesses(QRunnable):
    def __init__(self, textBrowser):
        super(AuthenticatorProcesses, self).__init__()
        self.textBrowser = textBrowser
        print("created new authenticator object processes")
        self.textBrowser.append("created new authenticator object processes")
        #self.initializeParameters()
    
    async def run_client(self) -> None:
        reader, writer = await asyncio.open_connection(HOST, PORT)

        writer.write(b"Authentication Message!")
        await writer.drain()

        # messages = 4

        while True:
            
            self.dic = {'apnonce':os.urandom(32),'β':True,'channelinfo':1,'apmac':b'\x11\x22\x33\x44\x55\x66'}
            self.message1 = pickle.dumps(self.dic)
            print(type(self.message1))
            
            writer.write(self.message1)
            await writer.drain()
            # self.client.send(self.message1)
            self.textBrowser.append("message 1 sent successfully")
            await asyncio.sleep(1)
            
            
            # Receive message from Suplicant
            data = await reader.read(1024)

            # print(f"Received: {data.decode()!r}")
            # self.textBrowser.append(f"Received: {data.decode()!r}")

            # try:
            #     self.dic3 = pickle.loads(data)
            #     print("msg ::  ")
            #     print(self.dic3)
            #     self.spnonce = self.dic3.get('spnonce')
            #     self.spmac = self.dic3.get('smac')
            #     #print('supplicants nonce:'+str(self.spnonce))
            #     #print('supplicants mac address:'+str(self.spmac))
            #     self.PTK = (self.generate_pmk().hex()+self.spnonce.hex()+self.spmac.hex()+self.apMacAddress()+self.apNonce().hex())
            #     self.textBrowser.append('Authenticators PTK:'+self.PTK[0:96])
            #     self.textBrowser.append('Key Confirmation Key (KCK):'+self.PTK[0:32])
            #     self.textBrowser.append('Key Encryption Key (KEK):'+self.PTK[32:64])
            #     self.textBrowser.append('Temporal Key (TK):'+self.PTK[64:96])
            #     self.gtk = os.urandom(32)

            #     self.dic4 = {'gtk':self.gtk, 'channelinfo':1, 'apmac':b'\x11\x22\x33\x44\x55\x66', 'apnonce':os.urandom(32)}
            #     self.message3 = pickle.dumps(self.dic4)
            #     writer.write(self.message1)
            #     await writer.drain()
            #     # self.client.send(self.message3)
            #     self.textBrowser.append('message 3 sent successfully')
            #     self.textBrowser.append('The group Temporal key is: '+self.gtk[0:32].hex())
            #     await asyncio.sleep(1)

            #     # self.response=self.client.recv(1024)
            #     self.response = await reader.read(1024)
            #     self.textBrowser.append(self.response.decode())
            #     self.textBrowser.append('Four way Handshake completed, PTK installed on the authenticator')
            # except Exception as e:
            #     print("Exception was raised")
            #     print("Exited System")
            #     print(f"An exception occurred: {str(e)}")




            await asyncio.sleep(3)
            writer.write(b"quit")
            await writer.drain()
            writer.close()
            break


    @Slot()
    def run(self):
        print("beginning of Authenticator program")
        self.textBrowser.append("beginning of Authenticator program")
        asyncio.run(self.run_client())
        print("end of authenticator program")
        self.textBrowser.append("end of authenticator program")
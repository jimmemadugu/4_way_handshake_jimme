from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import hmac
import hashlib
import os
import socket
import pickle
from PyQt5.uic import loadUiType
ui,_=loadUiType('accesspoints.ui')
class MainApp(QMainWindow,ui):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.displayParameters()
		self.pushButton_authenticator.clicked.connect(self.authenticator)
		
	def authenticator(self):
		
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client.connect((socket.gethostname(),8080))
		self.textBrowser.append('connection Established')
		while True:
			try:	
				self.dic={'apnonce':os.urandom(32),'β':True,'channelinfo':1,'apmac':b'\x11\x22\x33\x44\x55\x66'}
				self.message1=pickle.dumps(self.dic)
				self.client.send(self.message1)
				self.textBrowser.append("message1 sent successfully")
				self.bytedic1 = self.client.recv(1024)
				self.dic3=pickle.loads(self.bytedic1)
				self.spnonce=self.dic3.get('spnonce')
				self.spmac=self.dic3.get('smac')
				#print('supplicants nonce:'+str(self.spnonce))
				#print('supplicants mac address:'+str(self.spmac))
				self.PTK=(self.generate_pmk().hex()+self.spnonce.hex()+self.spmac.hex()+self.apMacAddress()+self.apNonce().hex())
				self.textBrowser.append('Authenticators PTK:'+self.PTK[0:96])
				self.textBrowser.append('Key Confirmation Key (KCK):'+self.PTK[0:32])
				self.textBrowser.append('Key Encryption Key (KEK):'+self.PTK[32:64])
				self.textBrowser.append('Temporal Key (TK):'+self.PTK[64:96])
				self.gtk=os.urandom(32)
				self.dic4={'gtk':self.gtk, 'channelinfo':1, 'apmac':b'\x11\x22\x33\x44\x55\x66', 'apnonce':os.urandom(32)}
				self.message3=pickle.dumps(self.dic4)
				self.client.send(self.message3)
				self.textBrowser.append('message3 sent successfully')
				self.textBrowser.append('The group Temporal key is:'+self.gtk[0:32].hex())
				self.response=self.client.recv(1024)
				self.textBrowser.append(self.response.decode())
				self.textBrowser.append('Four way Handshake completed, PTK installed on the authenticator')
			except Exception as e:
				self.textBrowser.append("exception"+str(e))
			#self.client.close()
			break
	

	def displayParameters(self):
		self.apnonce=self.apNonce()
		self.amac= self.apMacAddress()
		self.smac=self.clientMacAddress()
		self.l01.setText("Initializing Authenticators parameters...")
		self.l01.append("APs Nonce="+str(self.apnonce.hex()))
		self.l01.append("supplicants Mac address="+self.smac)
		self.l01.append("APs Mac address="+self.amac)
		self.pmk=self.generate_pmk()
		self.l01.append("APs pmk="+str(self.pmk.hex()))
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

def main():
	app=QApplication(sys.argv)
	window=MainApp()
	window.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()

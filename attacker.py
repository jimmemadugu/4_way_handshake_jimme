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
ui,_=loadUiType('attacker.ui')
class MainApp(QMainWindow,ui):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.pushButtonAttacker.clicked.connect(self.attacker)
	def attacker(self):
		
		self.attack = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.attack.connect((socket.gethostname(),8080))
		self.textBrowser.append('connection Established')
		while True:
			self.csa={'apnonce':os.urandom(32),'β':True,'channelinfo':2,'apmac':b'\x11\x22\x33\x44\x55\x66'}
			self.CSA=pickle.dumps(self.csa)
			self.attack.send(self.CSA)
			self.msg=self.attack.recv(1024)
			try:
				self.decoded_string = self.msg.decode('utf-8')
				self.textBrowser.append(self.decoded_string)
			except UnicodeDecodeError as e:
				# Handle the error
				self.decoded_string = self.msg.decode('utf-8', errors='replace')
				self.textBrowser.append(self.decoded_string)
			self.msg1=self.attack.recv(1024)
			self.textBrowser.append(self.msg1.decode())
			#print(self.msg1.decode())
			break
def main():
	app=QApplication(sys.argv)
	window=MainApp()
	window.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()

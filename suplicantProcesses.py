import os
# import sys
# import hmac
import hashlib

class SuplicantProcesses:
    def __init__(self):
        print("started new supplicant object processes")
        self.initializeParameters()
    
    def initializeParameters(self):
        print("displaying supplicant object parameters")
        self.spnonce=self.spNonce()
        self.amac= self.apMacAddress()
        self.smac=self.clientMacAddress()
        self.pmk=self.generate_pmk()

    def returnParametersString(self):
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
    
    # def runSupplicantProcesses(self, is_running):
    #     self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     self.server_socket.bind((socket.gethostname(),8080))
    #     self.server_socket.listen(5)
    #     self.sockets_list = [self.server_socket]
    #     "Client started. Waiting for connections..."

import asyncio
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

        messages = 4

        while True:
            data = await reader.read(1024)

            print(f"Received: {data.decode()!r}")
            self.textBrowser.append(f"Received: {data.decode()!r}")

            if messages > 0:
                await asyncio.sleep(1)
                writer.write(f"{time.time()}".encode())
                await writer.drain()
                messages -= 1
            else:
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
import socket
import pickle

from utils.logger import log

BUFFERSIZE = 1024


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 7777
        self.address = (self.server_ip, self.port)

    def __del__(self):
        self.closeConnection()

    def getAddress(self):
        return self.socket.getsockname()

    def handShake(self, code):
        # Give code to the server
        self.send(code)
        status_code = self.recieve()
        # Check response from server
        if not (status_code == 200) or (status_code == 444):
            self.closeConnection()
            return False
        else:
            self.send(200)
            return True

    def connect(self):
        try:
            self.socket.connect(self.address)
            self.socket.getsockname()
            data = self.recieve()
            if data == 200:
                return True
            else:
                self.closeConnection()
                return False
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()

    def send(self, data):
        try:
            self.socket.sendall(pickle.dumps(data))
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()

    def recieve(self):
        try:
            return pickle.loads(self.socket.recv(BUFFERSIZE))
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()
            return ""

    def closeConnection(self):
        log(__name__, "Closing connection", "info")
        self.socket.close()

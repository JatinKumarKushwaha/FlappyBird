import socket
import pickle

from random import randrange
from utils.logger import log

MAX_CLIENTS = 2
BUFFERSIZE = 1024


class Server:
    def __init__(self) -> None:
        self.MAX_CLIENTS = MAX_CLIENTS
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip: str = socket.gethostbyname(socket.gethostname())
        self.port: int = 7777
        self.server_address = (self.server_ip, self.port)
        self.clients = []  # Stores tuples of type (client_socket, client_address)

        code = self.generateCode()
        self.code = code

    def __del__(self):
        self.closeConnection()

    def getCode(self):
        return self.code

    def generateCode(self):
        code = randrange(100000, 1000000)
        return code

    def listen(self):
        try:
            self.server_socket.bind(self.server_address)
            self.server_socket.listen(MAX_CLIENTS)
            log(__name__, "Waiting for connection...", "info")

            return True
        except socket.error as e:
            log(__name__, e, "error")
            return False

    def accept(self):
        try:
            (conn, addr) = self.server_socket.accept()
            log(__name__, "Connected to " + str(addr), "info")
            self.clients.append((conn, addr))
            if conn:
                conn.send(pickle.dumps(200))
            return (conn, addr)
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()

    def handShakeWithAddress(self, address):
        log(__name__, "Performing handshake with " + str(address), "info")
        log(__name__, "Checking for valid connection", "info")
        # Receive code from client
        client_code = self.receiveFromAddress(address)

        if int(client_code) == self.code:
            self.sendToAddress(address, 200)
            log(__name__, "Connection valid", "info")
            return True
        else:
            log(__name__, "Incorrect code", "warn")
            self.sendToAddress(address, 444)
            self.closeConnection()
            return False

    def sendAll(self, data):
        try:
            for client in self.clients:
                client[0].sendall(pickle.dumps(data))
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()

    def sendToAddress(self, address, data):
        try:
            for client in self.clients:
                if client[1] == address:
                    client[0].sendall(pickle.dumps(data))
                    return
            log(__name__, "Invalid address", "warn")
            return
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()

    def receiveFromAddress(self, address):
        try:
            connection = None
            for client in self.clients:
                if client[1] == address:
                    connection = client[0]
                    log(__name__, "Receiving from " + str(client[1]), "info")
            if connection == None:
                log(__name__, "Invalid address", "warn")
                return pickle.dumps(404)
            return pickle.loads(connection.recv(BUFFERSIZE))
        except socket.error as e:
            log(__name__, e, "error")
            self.closeConnection()
            return 0

    def receiveFromAll(self):
        data = []
        for client in self.clients:
            data.append(self.receiveFromAddress(client[1]))
        return data

    def closeConnection(self):
        log(__name__, "Closing connection", "info")
        for client in self.clients:
            client[0].close()
        self.server_socket.close()

import socket  # Import socket module
from typing import Callable


class BaseStationSock():

    def __init__(self, host: str = '127.0.0.1', port: int = 50000, numCon: int = 1) -> None:

        # create socket object and set it to ignore if the socket is already in use
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.HOST = host
        self.PORT = port
        self.NUMC = numCon

        # This will be called when a connection is found so that

    def on_new_client(self, clientsocket: socket.socket, addr):
        while True:
            msg = input('SERVER >> ')
            if not msg:
                exit()
            # Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
            clientsocket.sendall(msg.encode('UTF-8'))
            # number of connections

    def start_listen(self):

        self.sock.bind((self.HOST, self.PORT))        # Bind to the port
        # Now wait for client connection.
        self.sock.listen(self.NUMC)

        print(f'Server started on {self.HOST}:{self.PORT}')
        print('Waiting for clients...')

        threads = []
        for i in range(self.NUMC):
            # Establish connection with client.
            conn, addr = self.sock.accept()
            self.newConnHandler(conn, addr)

    def setCallable(self, callback: Callable[[socket.socket, tuple], None]):
        self.newConnHandler = callback

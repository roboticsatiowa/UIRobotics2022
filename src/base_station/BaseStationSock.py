import socket  # Import socket module
from typing import Callable


class BaseStationSock:

    def __init__(self,
                 callback: Callable = None,
                 addr: tuple[str, int] = ('localhost', 50000),
                 numconn: int = 1) -> None:
        # create socket object
        self.newConnHandler = callback
        self.sock = socket.socket()

        # overides socket if already in use
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.addr = addr  # ip and port number
        self.NUMC = numconn  # number of connections to open

    def start_listen(self):
        self.sock.bind(self.addr)  # Bind to the port
        # Now wait for client connection.
        self.sock.listen(self.NUMC)

        print(f'Server started on {self.addr}')
        print('Waiting for clients...')

        for i in range(self.NUMC):
            # Establish connection with client.
            conn, addr = self.sock.accept()
            self.newConnHandler(conn, addr)

    def set_callback(self, callback: Callable[[socket.socket, tuple], None]):
        self.newConnHandler = callback

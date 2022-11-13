import socket
from typing import Callable


class RoverSock:

    def __init__(self, callback: Callable = None, addr: tuple[str, int] = ('localhost', 50000)):
        self.newConnHandler = callback
        self.addr = addr
        self.socks = dict()
        self.add_socket("main")
        self.add_socket("video")
        self.add_socket("audio")
        self.add_socket("gps")

    def add_socket(self, socket_name):
        self.socks[socket_name] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        for sock_name in self.socks:
            sock = self.socks[sock_name]
            sock.connect(self.addr)
            sock.sendall(sock_name.encode("UTF-8"))
            self.newConnHandler(sock, sock_name)

    def set_callback(self, callback: Callable[[socket.socket, str], None]):
        self.newConnHandler = callback

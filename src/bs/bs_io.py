import pickle
import socket  # Import socket module
import struct
import threading
from typing import Callable

import cv2

import skeletonGUI

threads = dict()


class BaseStationSock:

    def __init__(self,
                 callback: Callable = None,
                 addr: tuple[str, int] = ('localhost', 50000),
                 numconn: int = 1):
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


def read_video_stream(conn: socket.socket, addr: tuple) -> None:
    data = b''

    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = conn.recv(4 * 1024)
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        skeletonGUI.Window.set_video_frame(frame)
        cv2.imshow("Receiving...", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


def on_new_connection(conn: socket.socket, addr: tuple) -> None:
    conn_name = conn.recv(1024).decode("UTF-8")
    print(f'new data stream {conn_name.upper()} from {addr}')
    if conn_name == 'main':
        return
    if conn_name == 'video':
        thread = threading.Thread(target=read_video_stream, args=(conn, addr), daemon=True)
    else:
        return
    thread.start()
    threads[conn_name] = thread


def start_connection():
    # sets the handler for when a new connection is established by the socket
    sock_handler = BaseStationSock(numconn=4)
    sock_handler.set_callback(on_new_connection)

    # begin to listen for connections
    sock_handler.start_listen()

    # cleanup
    sock_handler.sock.close()


if __name__ == '__main__':
    start_connection()

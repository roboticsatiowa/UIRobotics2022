import pickle
import socket
import struct
import threading

import cv2
import imutils

from rover.RoverSock import RoverSock

threads = []


def send_video_stream(conn: socket.socket) -> None:
    print("starting video stream")
    vid = cv2.VideoCapture(0)
    while vid.isOpened():
        img, frame = vid.read()
        frame = imutils.resize(frame, width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        conn.sendall(message)


def on_new_connection(conn: socket.socket, conn_name: str) -> None:
    print(f'connected stream {conn_name}')
    if conn_name == 'video':
        thread = threading.Thread(target=send_video_stream, args=(conn,), daemon=True)
        thread.start()
        threads.append(thread)


sock_handler = RoverSock()

# sets the handler for when a new connection is established by the socket
sock_handler.set_callback(on_new_connection)

# begin to listen for connections
sock_handler.start_connection()

threads[0].join()

for sock_name in sock_handler.socks:
    sock_handler.socks[sock_name].close()

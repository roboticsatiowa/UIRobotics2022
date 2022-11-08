import pickle
import socket
import struct
import threading

import cv2

from base_station.BaseStationSock import BaseStationSock

threads = []

main_conn = None


def read_audio():
    pass


def read_gps_location():
    pass


def read_video_stream(conn: socket.socket, addr: tuple) -> None:
    print("video stream started")

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
        cv2.imshow("Receiving...", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


def on_new_connection(conn: socket.socket, addr: tuple) -> None:
    conn_name = conn.recv(1024)
    print(f'new connection from {addr} called {conn_name.decode("UTF-8")}')
    if conn_name == b'main':
        global main_conn
        main_conn = conn
    if conn_name == b'video':
        thread = threading.Thread(target=read_video_stream, args=(conn, addr), daemon=True)
    else:
        return
    thread.start()
    threads.append(thread)


sock_handler = BaseStationSock(numconn=4)

# sets the handler for when a new connection is established by the socket
sock_handler.set_callback(on_new_connection)

# begin to listen for connections
sock_handler.start_listen()

input("Enter any key to end")

# cleanup
cv2.destroyAllWindows()
sock_handler.sock.close()

import socket
import threading

from base_station.BaseStationSock import BaseStationSock

threads = []

main_conn = None


def read_audio():
    pass


def read_gps_location():
    pass


def read_video_stream(conn: socket.socket, addr: tuple) -> None:
    print("video stream started")


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


socket = BaseStationSock(numconn=4)

# sets the handler for when a new connection is established by the socket
socket.set_callback(on_new_connection)

# begin to listen for connections
socket.start_listen()

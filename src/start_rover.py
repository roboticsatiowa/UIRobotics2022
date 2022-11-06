import socket

from rover.RoverSock import RoverSock


def send_video_stream(conn: socket.socket, addr: tuple) -> None:
    print("video stream started")


def on_new_connection(conn: socket.socket, conn_name: str) -> None:
    print(f'connected stream {conn_name}')


sock_handler = RoverSock()

# sets the handler for when a new connection is established by the socket
sock_handler.set_callback(on_new_connection)

# begin to listen for connections
sock_handler.start_connection()

for sock_name in sock_handler.socks:
    sock_handler.socks[sock_name].close()

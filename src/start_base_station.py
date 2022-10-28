import socket

from base_station.BaseStationSock import BaseStationSock


def onNewConnection(conn: socket.socket, addr: tuple) -> None:
    print(f'new connection from {addr}')


socket = BaseStationSock()
socket.setCallable(onNewConnection)

socket.start_listen()

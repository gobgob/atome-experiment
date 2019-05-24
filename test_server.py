#!/usr/bin/python3

# inspired from https://www.binarytides.com/python-socket-server-code-example/

import socket
import select
import time

if __name__ == "__main__":

    RECV_BUFFER = 4096
    PORT = 8766

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))

    counter = 5
    while counter > 0:
        print("Starting match in " + str(counter))
        counter -= 1
        time.sleep(1)

    server_socket.listen()
    print("Server started on port " + str(PORT))

    while True:
        sockfd, addr = server_socket.accept()
        print("Client (%s, %s) connected" % addr)
        sockfd.close()

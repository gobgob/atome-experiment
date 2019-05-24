#!/usr/bin/python3

# inspired from https://www.binarytides.com/python-socket-server-code-example/

import socket
import select

if __name__ == "__main__":

    conn_list = []
    RECV_BUFFER = 4096
    PORT = 8766

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
    conn_list.append(server_socket)

    print("Server started on port " + str(PORT))

    while True:
        read_socks, write_socks, error_socks = select.select(conn_list, [], [])

        for sock in read_socks:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                conn_list.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                sockfd.send("START\n".encode("ascii"))
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    print(data)
                    # if str(data)==ASK_STATUS:
                    #   sock.send("START\n".encode("ascii"))
                except:
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    conn_list.remove(sock)
                    continue

    server_socket.close()

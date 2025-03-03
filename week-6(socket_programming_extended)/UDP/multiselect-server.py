WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
import socket
from argparse import ArgumentParser
import select
from time import sleep

def parse_args():
    # parse the command line arguments
    args = ArgumentParser()
    args.add_argument('--host', default="127.0.0.1")
    args.add_argument('--port', default=8000, type=int)
    return args.parse_args()

def start_multi_tcp_server(host, port):
    # create a server socket with the following specifications
    #   AF_INET -> IPv4 socket
    #   SOCK_STREAM -> UDP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

        # bind the socket to a OS port
        server_socket.bind((host, port))

        # set socket as non-blocking so calls dont block forever
        server_socket.setblocking(False)

        # configure sources of input and output
        #   server_socket input means a new connection
        inputs = [server_socket]
        # we will populate outputs as new clients connect
        outputs = []

        # create a list of client connections to keep track of their data
        clients = {}
        client_id = 0

        # while we still have inputs to read from
        while inputs:

            # select.select(param1, param2, param3, timeout) takes three parameters and returns three lists
            #   param1 -> file descriptors we can read from (e.g., server sockets, client sockets)
            #   param2 -> file descriptors we can write to (e.g., client sockets)
            #   param3 -> file descriptors that can throw exceptions (e.g., client sockets on disconnect)
            #   timeout -> timeout for non-block
            # The return values are sub-lists of the three parameters that contain 
            # the file descriptors that are ready for the corresponding operation
            # readables is a sub-list of param1 (inputs) that contains sockets that are ready for reading
            # writables is a sub-list of param2 (outputs) that contains sockets that are ready for writing
            # exceptionals is a sub-list of param3 (inputs) that contains sockets that have errored out
            readables, writables, exceptionals = select.select(inputs, outputs, inputs, 1)


            # iterate over readable sockets and handle accordingly
            for sock in readables:

              # get client from clients dictionary
              # receive message from client
              message, addr = sock.recvfrom(1024)
              message = message.decode()

              if addr not in clients:
                clients[addr] =

              # set client ping to True so we can respond
              if message and "Ping" in message:
                  # print message from client
                  print(f"Message from {client.addr}: {message}")
                  client.hasPinged = True
              else:
                  # if empty message, disconnect client
                  inputs.remove(sock)
                  outputs.remove(sock)
                  sock.close()


            # iterate over writable sockets and handle
            for sock in writables:
                # writables will always be a client socket

                # get client from clients dictionary
                client = clients[sock]

                # check if client has pinged and is expecting a pong
                if client.hasPinged:
                    # send pong
                    sock.sendall(f"Pong #{client.pongCount}".encode())
                    # increment count of pong
                    client.pongCount += 1
                    # set hasPinged to False
                    client.hasPinged = False


            # iterate over exception sockets and handle
            for sock in exceptionals:
                inputs.remove(sock)
                outputs.remove(sock)
                del clients[sock]
                sock.close()




if __name__ == '__main__':
    # parse command line arguments
    args = parse_args()

    # start the tcp server
    start_multi_tcp_server(args.host, args.port)
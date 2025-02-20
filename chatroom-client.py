# Python program to implement client side of chat room. 
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((IP_address, port))

while True:

	# maintains a list of possible input streams 
    sockets_list = [server]
    
    # Helps for determining whether a message needs to be sent from a user or if the server wants to send a message
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print (message.decode())
        else:
            #message = input("Enter your message: ")
            message = sys.stdin.readline()
            print("<You>" + message)
            server.send(message.encode())
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()

# UDPPingerClient.py
from socket import *
#Imports specific modules from the time package to facilitate the program's round trip calculation purpose
from time import time, ctime
#Stores the IP address of the machine to run the server
serverIP = '192.168.56.101'
#Stores the port number that the client will connect to on the server
serverPort = 12000
# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
#Sets a timeout that waits one second to receive a response from the server
clientSocket.settimeout(1)
#Sends 10 messages to the server
for i in range(10):
    try:
        #Stores the time in seconds from the epoch to now (when the message is sent)
        startTime = time()
        #Sends a message to the server specified by the server's IP adress and a given port number
        clientSocket.sendto(('Ping ' + str(i+1) + ' ' + ctime(startTime)).encode(), (serverIP, serverPort))
        #Potentially receives a message and the server's adresss from the server
        message, serverAddress = clientSocket.recvfrom(1024)
        #Stores the time in seconds from the epoch to now (when the response message is potentially received
        endTime = time()
        #Prints the message that was potentially received from the server (a decoded version)
        print('Message response: ' + message.decode())
        #Prints the round trip time of the messahe that was potentially received from the server
        print('RTT: %.3f ms\n' % ((endTime - startTime)* 1000) )
    except timeout:
        #Prints an error message if the message from the client was "lost" on it's way to the server
        print('Request timed out\n')
#Closes the socket connection
clientSocket.close()
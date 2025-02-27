#!/usr/bin/python3

# Simple "RDT over UDP" protocol sender
# See rdt.py for the packet format

from socket import *
from rdt import *
from queue import SimpleQueue
import sys, json

# Get receiver IP and port from command line arg. Default to localhost, port 12000
receiverIP = '127.0.0.1'
receiverPort = 12000
try:
    receiverIP = sys.argv[1]
    receiverPort = int(sys.argv[2])
except IndexError:
    pass

# Set up a queue as a send buffer. From std. Python library
q = SimpleQueue()

# Data to send: "We want to test this reliable data transfer protocol."
data = [ 'We', 'want', 'to', 'test', 'this', 'reliable', 'data', 'transfer', 'protocol', '.' ]
for c in data:
    q.put(c)
n_pkts = q.qsize()

# Initialize sender state
base = 1
nextseqnum = 1

# Sender needs to handle four events:
# 1. Send app data
# 2. Handle recv ACK packet (notcorrupt)
# 3. Handle recv ACK packet (corrupt)
# 4. Handle timeout

# Simple timeout mechanism, recvfrom() will timeout after 3 seconds
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3)

# Keep sending/waiting until we have nothng else to send or
# we have no more acks expected
while not q.empty() or (base < n_pkts):

    # The first 'event' we have to handle is sending app data
    if not q.empty():
        # Get some data from the send buffer and make a packet
        packet = make_data_pkt(nextseqnum, q.get())
        print('\nSending ' + str(packet))
        nextseqnum += 1

        # Send the packet using our underlying 'unreliable' transport
        # 'packet' must be a dict, as specified in the 'packet format' in rdt.py
        udt_send(clientSocket, packet, (receiverIP, receiverPort))

    # Wait for a response. We expect either an ACK packet,
    # or we wait for a timeout event. If we get a packet, the timer stops.
    ack_received = False
    while not ack_received:
        try:
            # The underlying recvfrom() will timeout after 3 seconds
            packet, peer = rdt_rcv(clientSocket)

        # Handle timeout condition here
        except timeout:
            # Retransmit last packet. udt_send() restarts timer
            udt_send(clientSocket, packet, (serverIP, serverPort))
            print('Timeout, retransmitting ' + str(packet))
            continue
        else:
            # We have received an ACK packet
            ack_received = True
            print('Received ' + str(packet))
            if notcorrupt(packet):
                base = getacknum(packet)+1
            else:
                print('RECEIVED CORRUPT ACK')

clientSocket.close()

# Optional enhancement:
#   What happens when you run the sender a second time without restarting the receiver?
#   How can you fix this? Hint: How does TCP handle this?

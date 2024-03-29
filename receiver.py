import sys
from socket import *
from helper import *
import json
import random
import heapq

# verify number of arguments passed in from command line
n = len(sys.argv)

if n != 4:
    # print error and exit if incorrect number of arguments
    print("Must pass 3 arguments, Total arguments passed:", n - 1)
    exit()

try:
    n_port = int(sys.argv[1])
except:
    # print error message and exit if n_port cannot be converted to an integer
    print("n_port is not an integer")
    exit()

try:
    prob = float(sys.argv[2])
except:
    # print error message and exit if prob cannot be converted to a float
    print("probability is not a float")
    exit()

try:
    file_name = str(sys.argv[3])
except:
    # print error message and exit if file_name cannot be converted to a string
    print("file_name is not a string")
    exit()

#create priority queue for packets
q = []

#keep track of next expected sequence number
next_expected_packet = 0

# open files for logging
f_arrival = open('arrival.log', 'w')
f_drop = open('drop.log', 'w')
f_data = open(file_name, 'w')

print("The receiver is ready for packets")

while True:

    try:
        # create UDP socket
        UDPSocket = socket(AF_INET, SOCK_DGRAM)

        # bind UDP socket to input port
        UDPSocket.bind(('', n_port))
    except:
        print("n_port is unavailable")
        exit()

    # wait for message from UDP client
    message, clientAddress = UDPSocket.recvfrom(2048)

    # convert from json to dictionary
    data_loaded = json.loads(message.decode())

    type = int(data_loaded["type"])
    seq_num = data_loaded["seqnum"]

    # log packet arrival
    f_arrival.write(str(seq_num) + '\n')

    # data type
    if type == 1:

        # drop with probability
        drop = random.random() < prob

        if drop:
            # log drop
            f_drop.write(str(seq_num) + '\n')
            continue

        # send ack to client
        msg = {
          "type": "0",
          "seqnum": seq_num,
          "length": "0",
          "data": ""
        }

        encoded_json = json.dumps(msg)
        UDPSocket.sendto(encoded_json.encode(), clientAddress)
        UDPSocket.close()

        # add packet to queue
        heapq.heappush(q, (seq_num, data_loaded))

        # process queue while it is not empty and the packet with the smallest 
        # seq_num is either the next_expected_packet or it is a duplicate
        while len(q) > 0 and q[0][0] <= next_expected_packet:
            packet = heapq.heappop(q)

            # check if duplicate and already processed
            if packet[0] < next_expected_packet:
                continue

            # get packet info
            d = packet[1]

            f_data.write(d["data"])
            next_expected_packet += int(d["length"])


    # EOT, close connection
    elif type == 2:

        # send EOT back
        msg = {
          "type": "2",
          "seqnum": seq_num,
          "length": "0",
          "data": ""
        }

        # send EOT message to client
        encoded_json = json.dumps(msg)
        UDPSocket.sendto(encoded_json.encode(), clientAddress)
        UDPSocket.close()

        # save files, exit
        f_arrival.close()
        f_drop.close()
        f_data.close()

        break
    else:
        print("wrong message type")
        exit()

import os
import sys
import json
from multiprocessing import Process
from socket import *
from helper import *

class Server:
    def __init__(self):
        # Verifying the number of supplied arguments
        if len(sys.argv) != 6:
            printexit("usage: python sender.py <receiver_address> <receiver_port> <sender_port> <timeout> <filename>\n"
                "ERROR: requires 5 arguments, got {}".format(len(sys.argv)-1))
        
        # Validating the type of the supplied arguments
        self.receiver_address = sys.argv[1]
        self.filename = sys.argv[5]
        try:
            self.receiver_port = int(sys.argv[2])
            self.sender_port = int(sys.argv[3])
            self.timeout = int(sys.argv[4])
        except ValueError as e:
            printexit(f"ERROR: <receiver_port>={sys.argv[2]}, <sender_port>={sys.argv[3]} and <timeout>={sys.argv[4]} must be integers :: {e}")
        
        self.acked = dict()
        self.receiver = (self.receiver_address, self.receiver_port)
    
    def Setup_UDP_Socket(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        try:
            self.sock.bind(('', self.sender_port))
            print("The sender is ready to receive")
        except error as e:
            printexit(f"ERROR: failed to setup the UDP socket :: {e}")

    def Send_Packet(self):
        # Initializes the seqnum
        seqnum = 0

        # Reads data from <filename> and sends up to 500 characters
        # worth of data until reaching EOF
        with open(self.filename) as f:
            data = f.read(500)
            while data != "":
                # Creating new entry for this seqnum
                if seqnum not in self.acked:
                    self.acked[seqnum] = False

                # Checking if this packet needs to be sent
                if self.acked[seqnum] == False:
                    packet = {
                        'type': 1,
                        'seqnum': seqnum,
                        'length': len(data),
                        'data': data
                    }
                    s = json.dumps(packet) # serialized json from dict
                    self.sock.sendto(s.encode(), self.receiver)
                
                # Recording the sent packet
                Write_Log("seqnum.log", seqnum)

                # Retrieving new file data
                seqnum += len(data)
                data = f.read(500)
    
    def Wait_Timeout(self):
        # Wait until all packets are received and acknowledged
        while all(value == True for value in self.acked.values()):
            message, _ = self.sock.recvfrom(2048)
            ds = json.loads(message.decode()) # deserialized dict from json
            if ds['type'] == 0 and self.acked[ds['seqnum']] == False:
                self.acked[ds['seqnum']] = True
                Write_Log("ack.log", ds['seqnum'])   
    
    def Send_EOT(self):
        # Creating the EOT packet
        packet = {
            'type': 2,
            'seqnum': -1,
            'length': 0,
            'data': ""
        }

        # Sending the EOT packet
        s = json.dumps(packet) # serialized json from dict
        self.sock.sendto(s.encode(), self.receiver)

        # Receiving the EOT packet
        message, _ = self.sock.recvfrom(2048)
        ds = json.loads(message.decode()) # deserialized dict from json
        assert ds['type'] == 2 and ds['length'] == 0
        Write_Log("ack.log", ds['seqnum'])


def main():
    # Remove the log files if it exists
    if os.path.exists("seqnum.log"):
        os.remove("seqnum.log")
    
    if os.path.exists("ack.log"):
        os.remove("ack.log")

    # Creates a new sender object
    sender = Server()
    sender.Setup_UDP_Socket()
    while True:
        # Send the unacked packets
        sender.Send_Packet()

        # Creating a thread to receive acks until timeout
        p = Process(target=sender.Wait_Timeout)
        p.start()

        # Wait for timeout or until the process finishes
        p.join(int(round(sender.timeout / 1000)))

        # Check if the thread is still active
        if p.is_alive():
            print("Timeout occurred... Resending packets")
            p.terminate()
            p.join()
            continue

        # All packets are successfully acked
        break

    # Sends the EOT signal
    # Waits for the receiver until exiting
    sender.Send_EOT()

if __name__ == "__main__":
    main()
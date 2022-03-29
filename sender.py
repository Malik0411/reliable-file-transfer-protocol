import sys
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
        
        self.seqnum = 0
        self.receiver = (self.receiver_address, self.receiver_port)
    
    def Setup_UDP_Socket(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        try:
            self.sock.bind(('', self.sender_port))
            print("The sender is ready to receive")
        except error as e:
            printexit(f"ERROR: failed to setup the UDP socket :: {e}")

    def Send_Packet(self):
        # Reads data from <filename> and sends up to 500 characters
        # worth of data until reaching EOF
        f = open(self.filename)
        data = f.read(500)
        while data != "":
            packet = f"{1}\n{self.seqnum}\n{len(data)}\n{data}"
            self.sock.sendto(packet.encode(), self.receiver)
            self.seqnum += len(data)
            data = f.read(500)
        f.close()


def main():
    sender = Server()
    sender.Setup_UDP_Socket()

if __name__ == "__main__":
    main()
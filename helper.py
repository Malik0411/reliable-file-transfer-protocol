import sys

# Helper function:
# Writes a seqnum to a log file
def Write_Log(filename, seqnum):
    with open(filename, "a") as f:
        f.write(f'{seqnum}\n')

# Helper function:
# To print a message and exit the program
def printexit(msg):
    print(msg)
    sys.exit(0)
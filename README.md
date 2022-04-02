# Reliable file transfer protocol

## Running the programs

All of the code was written and run with Python 3.\
receiver.py must be started before sender.py

### Receiver

Command to run the receiver:\
python3 receiver.py <n_port> <probability> <output_file_name>

where 
**n_port_receiver** = UDP port number used by the receiver to receive data from the sender\
**probability** = drop probability\
**output_file_name** = name of the file into which the received data is written

eg. python3 receiver.py 12001 0.2 output\

This was tested on **ubuntu2004-002**\


### Sender

Command to run the sender:\
python3 sender.py <address> <n_port_receiver> <n_port_sender> <timeout> <file_name>\

**address** = host address of the receiver\
**n_port_receiver** = UDP port number used by the receiver to receive data from the sender\
**n_port_sender** = UDP port number used by the sender to send data and receive ACKs from the receiver.\
**timeout** = timeout interval in milliseconds.\
**file_name** = name of the file to be transferred.

eg. python3 sender.py ubuntu2004-002 12001 12001 1000 file.txt

This was tested on **ubuntu2004-004**\

# Reliable file transfer protocol

**Malik Omar Salvosa** (WatIAM: *MOSALVOS*, ID: *20677744*)

**Maria Zhang** (WatIAM: *M357ZHAN*, ID: *20748228*)

## Running the programs

All of our code was written and run with Python 3.\
`receiver.py` must be started before `sender.py`

### Receiver
Command to run the receiver:
```
python3 receiver.py <n_port> <probability> <file_name>
```
where,
1. **port_receiver**: UDP port number used by the receiver to receive data from the sender
2. **probability**: Drop probability
3. **file_name**: Name of the file into which the received data is written

An example execution of the receiver is:
```
python3 receiver.py 12001 0.2 output
```
This was tested on **ubuntu2004-002**

### Sender
Command to run the sender:
```
python3 sender.py <address> <port_receiver> <port_sender> <timeout> <file_name>
```
where,
1. **address**: Address for `host1` (the receiver)
2. **port_receiver**: UDP port number used by the receiver to receive data from the sender
3. **port_sender**: UDP port number used by the sender to send data and receive ACKs from the receiver
4. **timeout**: Timeout interval in milliseconds
5. **file_name**: Name of the file to be transferred

An example execution of the sender is:
```
python3 sender.py ubuntu2004-002 12001 12001 1000 file.txt
```
This was tested on **ubuntu2004-004**

import socket
import json
from threading import Thread

# Reserve a port
PORT = 1099

#Relation of file names with the peer address
relation_file_names_peers = {}
relation_peers_address = {}

# Creation of a socket object
s = socket.socket()
print("Socket successfully created")

# Bind the localhost IP address to the port
s.bind(('', PORT))
print(f"Socket binded to {(PORT)}")

# Put the socket into listening mode
s.listen(5)
print("Socket is listening")


def process_message(socket: socket, address: tuple):
    """ Process Message """
    while True:
        # Receive request from the client
        request = json.loads(c.recv(1024).decode())

        # Check type of request
        match request["type"]:
            case "JOIN":
                relation_file_names_peers.update({request["address"]: request["filenames"]})
                relation_peers_address.update({address: request["address"]})
                c.send("JOIN_OK".encode())
                print(f'Peer {request["address"]} adicionado com arquivos {request["filenames"]}')

            case "SEARCH":
                peers_with_file = [peer for peer in relation_file_names_peers if request["filename"] in relation_file_names_peers[peer]]
                c.sendall(json.dumps(peers_with_file).encode())
                print(f'Peer {relation_peers_address[address]} solicitou arquivo {request["filename"]}')
                
            case "UPDATE":
                relation_file_names_peers[addr].extend(request.file_name)
                c.send("UPDATE_OK".encode())

while True:
    # Establish connection with client
    c, addr = s.accept()
    thread = Thread(target=process_message, args=(c, addr))
    thread.start()
import socket
import json

# Reserve a port
PORT = 1099

#Relation of file names with the peer address
relation_file_names_peers = {}

# Creation of a socket object
s = socket.socket()
print("Socket successfully created")

# Bind the localhost IP address to the port
s.bind(('', PORT))
print(f"Socket binded to {(PORT)}")

# Put the socket into listening mode
s.listen(5)
print("Socket is listening")

while True:
    # Establish connection with client
    c, addr = s.accept()

    # Receive request from the client
    request = json.loads(c.recv(1024).decode())
    print(request)

    # Check type of request
    match request["type"]:
        case "JOIN":
            relation_file_names_peers.update({request["address"]: request["filenames"]})
            c.send("JOIN_OK".encode())
            print(f'Peer {request["address"]} adicionado com arquivos {request["filenames"]}')

        case "SEARCH":
            peers_with_file = [peer for peer in relation_file_names_peers if request["filename"] in relation_file_names_peers[peer]]
            c.sendall(json.dumps(peers_with_file).encode())
            print(f'Peer {request["address"]} solicitou arquivo {request["filename"]}')
            
        case "UPDATE":
            relation_file_names_peers[addr].extend(request.file_name)
            c.send("UPDATE_OK".encode())
    
    # Close the connection with the client
    c.close()
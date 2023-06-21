import socket, pickle
from request_class import RequestClass

# Reserve a port
PORT = 1095

#Relation of file names with the peer address
relation_file_names_peers = {}

""" Server start to listen to the clients """
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
    print(f"Got connection from {addr}")

    # Receive request from the client
    request: RequestClass = pickle.loads(c.recv(4096))

    # Check type of request
    match request.type:
        case "JOIN":
            print(request.__dict__)
            relation_file_names_peers.update({addr, request.file_names})
            c.send("JOIN_OK".encode())
        case "SEARCH":
            peers_with_file = [peer for peer in relation_file_names_peers if peer.value == request.file_names[0]]
            c.send(peers_with_file.encode())
        case "UPDATE":
            relation_file_names_peers[addr].extend(request.file_names[0])
            c.send("UPDATE_OK".encode())

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break
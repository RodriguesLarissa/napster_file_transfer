import socket, pickle
from request_class import RequestClass


# Creation of a socket object
s = socket.socket()
print("Socket successfully created")

# Define the port to connect
PORT = 1099

# Connect to the server
s.connect(('', PORT))

# Creation of request to server
# request = RequestClass("JOIN", ["Teste.mp4", "Shrek.mp4"])
# request = RequestClass("SEARCH", ["Teste.mp4"])
request = RequestClass("UPDATE", ["Shrek.mp4"])
s.send(pickle.dumps(request))

# Receive data from the server and decoding to get the string
print(s.recv(4096).decode())

# Close the connection
s.close()

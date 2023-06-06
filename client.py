import socket

# Creation of a socket object
s = socket.socket()
print("Socket successfully created")

# Define the port to connect
port = 1099

# Connect to the server
s.connect(('', port))

# Receive data from the server and decoding to get the string
print(s.recv(1024).decode())

# Close the connection
s.close()

import socket

# Creation of a socket object
s = socket.socket()
print("Socket successfully created")

# Reserve a port
port = 1099

# Bind the localhost IP address to the port
s.bind(('', port))
print(f"Socket binded to {(port)}")

# Put the socket into listening mode
s.listen(5)
print("Socket is listening")

while True:
    # Establish connection with client
    c, addr = s.accept()
    print(f"Got connection from {addr}")

    # Send a thank you message to the client
    c.send("Thank you for connecting".encode())

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break

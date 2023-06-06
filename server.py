import socket

# Reserve a port
PORT = 1099

class RequestClass:
    """ Class that represents the request to server """
    def __init__(self, tipo: str):
        self.tipo = tipo

def start_server():
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
        request: RequestClass = s.recv(1024).decode()

        # Check type of request
        match request.type:
            case "JOIN":
                return "JOIN_OK"
            case "SEARCH":
                return ""
            case "UPDATE":
                return "UPDATE_OK"

        # Send a thank you message to the client
        c.send("Thank you for connecting".encode())

        # Close the connection with the client
        c.close()

        # Breaking once connection closed
        break

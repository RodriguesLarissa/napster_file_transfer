import socket
import json
from threading import Thread

class Server:
    """ Creation of server class """

    def __init__(self):
        """ Global variables of server class """
        self.relation_file_names_peers = {}
        self.relation_peers_address = {}
        self.socket_server = socket.socket()
        self.ip = ""
        self.port = 0

    def start(self):
        """ Start server application """
        #Server startup
        self.ip = input("Digite o ip: ")
        self.port = int(input("Digite a porta: "))
        self.socket_connection()
        self.thread()
        
    def socket_connection(self):
        """ Start of the connection with socket """
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.listen(5)

    def thread(self):
        """ Start connection with thread """
        while True:
            connection, addr = self.socket_server.accept()
            thread = Thread(target=self.process_message, args=(connection, addr))
            thread.start()    

    def process_message(self, socket_type: socket, address: tuple):
        """ Process message based on JOIN, SEARCH or UPDATE """
        while True:
            # Receive request from the client
            request = json.loads(socket_type.recv(4096).decode())

            # Check type of request
            match request["type"]:
                #Performs the JOIN request
                case "JOIN":
                    self.relation_file_names_peers.update({request["address"]: request["filenames"]})
                    self.relation_peers_address.update({address: request["address"]})
                    socket_type.send("JOIN_OK".encode())
                    print(f'Peer {request["address"]} adicionado com arquivos {request["filenames"]}')

                #Performs the SEARCH request
                case "SEARCH":
                    peers_with_file = [peer for peer in self.relation_file_names_peers if request["filename"] in self.relation_file_names_peers[peer]]
                    socket_type.sendall(json.dumps(peers_with_file).encode())
                    print(f'Peer {self.relation_peers_address[address]} solicitou arquivo {request["filename"]}')
                
                #Performs the UPDATE request
                case "UPDATE":
                    self.relation_file_names_peers[self.relation_peers_address[address]].append(request["filename"])
                    socket_type.send("UPDATE_OK".encode())

server = Server()
server.start()
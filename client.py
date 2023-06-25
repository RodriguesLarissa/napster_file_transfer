import socket
import json
import os
from threading import Thread

# Define port to connect with server
PORT = 1099

class Client:
    """ Creation of client class """

    def __init__(self):
        """ Global variables of client class """
        self.socket_server = socket.socket()
        self.socket_download = socket.socket()
        self.socket_send_file = socket.socket()
        self.folder_path = ""
        self.peer_ip = ""
        self.peer_port = 0
        self.listen_connections_thread = Thread(target=self.listen_connections)

    def join(self):
        """ Function to peer connect to the server """
        self.peer_ip = input("Digite o ip: ")
        self.peer_port = int(input("Digite a porta: "))
        peer_address = f"{self.peer_ip}:{self.peer_port}"
        self.folder_path = str(input(("Digite o nome da pasta com os arquivos: ")))
        filenames = self.get_filenames()

        self.connect_socket_send_file()

        self.socket_server.connect(('', PORT))
        message_to_server = {"type": "JOIN", "address": peer_address, "filenames": filenames}
        server_message = self.send_message_to_server(self.socket_server, message_to_server)

        if server_message == "JOIN_OK":
            print(f'Sou peer {peer_address} com arquivos {filenames}')

    def search(self):
        """ Function to search peers with files wanted """
        filename = str(input(("Digite o nome do arquivo que está procurando: ")))
        message_to_server = {"type": "SEARCH", "filename": filename}
        peer_addresses = self.send_message_to_server(self.socket_server, message_to_server)
        print(f'peers com arquivo solicitado: {json.loads(peer_addresses)}')

    def download(self):
        """ Function to download files from another peer """
        peer_ip = input("Digite o ip: ")
        peer_port = int(input("Digite a porta: "))
        filename = str(input(("Digite o nome do arquivo para download: ")))

        self.socket_download.connect((peer_ip, peer_port))
        message_to_server = {"type": "DOWNLOAD", "filename": filename}
        self.socket_download.sendall(json.dumps(message_to_server).encode())
        file = self.socket_download.recv(4096)
        self.write_file(file, filename)
        print(f'Arquivo {filename} baixado com sucesso na pasta {self.folder_path}')
        self.update(filename)

    def write_file(self, file, filename: str):
        """ Write file in folder """
        with open(f'{self.folder_path}/{filename}', 'wb') as file_to_write:
            while True:
                data = file
                if not data:
                    break
                file_to_write.write(data)
            file_to_write.close()

    def update(self, filename: str):
        """ Function to update informations of the peer on the server """
        message_to_server = {"type": "UPDATE", "filename": filename}
        self.send_message_to_server(self.socket_server, message_to_server)

    def send_message_to_server(self, socket_type: socket, message_to_server: dict):
        """ Connect """    
        socket_type.sendall(json.dumps(message_to_server).encode())
        return socket_type.recv(4096).decode()

    def get_filenames(self):
        """ Get filenames from folder path """
        filenames = []
        for filename in os.listdir(self.folder_path):
            filenames.append(filename)
        return filenames

    def listen_connections(self):
        """ Listen for connections"""
        while True:
            connection, _ = self.socket_send_file.accept()
            request = json.loads(connection.recv(4096).decode())

            if request["type"] ==  "DOWNLOAD" and request["filename"] in self.get_filenames():
                with open(f'{self.folder_path}/{request["filename"]}', "rb") as file_to_send:
                    bytes_read = file_to_send.read(4096)
                    if not bytes_read:
                        break
                    connection.sendall(bytes_read)
                    connection.close()

    def connect_socket_send_file(self):
        """ Create connection of socket """
        self.socket_send_file.bind((self.peer_ip, self.peer_port))
        self.socket_send_file.listen(5)
        self.listen_connections_thread.start()

    def start(self):
        """ Function with interactive menu to start the funcionality """
        while True:
            action = int(input('''Escolha uma ação:  
                1 - Join
                2 - Search
                3 - Download
            '''))

            match action:
                case 1: self.join()
                case 2: self.search()
                case 3: self.download()

client = Client()
client.start()

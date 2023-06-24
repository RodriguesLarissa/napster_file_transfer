import socket, pickle
import os
from threading import Thread

# Creation of a socket object
socket_server = socket.socket()
socket_peer = socket.socket()

# Define port to connect with server
PORT = 1099

def join():
    """ Join """
    peer_address = (input("Digite o ip: "), int(input("Digite a porta: ")))
    folder_path = str(input(("Digite o nome da pasta com os arquivos: ")))
    filenames = get_filenames(folder_path)
    message_to_server = {"type": "JOIN", "address": peer_address, "filenames": filenames}
    connect_to_server(message_to_server)
    print(f'Sou peer {peer_address[0]}:{peer_address[1]} com arquivos {filenames}')

def search():
    """ Search """
    filename = str(input(("Digite o nome do arquivo que está procurando: ")))
    peer_addresses = connect_to_server({"type": "SEARCH", "file_name": filename})
    print(f'peers com arquivo solicitado: {peer_addresses}')

def download():
    """ Download """
    peer_address = (input("Digite o ip: "), int(input("Digite a porta: ")))
    file_name = str(input(("Digite o nome do arquivo para download: ")))
    connect_to_server({"type": "DONWLOAD", "address": peer_address, "file_name": file_name})

def connect_to_server(message_to_server: dict):
    """ Connect """
    socket_server.connect(('', PORT))
    socket_server.send(pickle.dumps(message_to_server))
    return socket_server.recv(1024).decode()

def get_filenames(folder_path: str):
    """ Get filenames """
    filenames = []
    for filename in os.listdir(folder_path):
        filenames.append(filename)
    return filenames

action = int(input('''Escolha uma ação:  
    1 - Join
    2 - Search
    3 - Download
'''))

while True:
    match action:
        case 1: join()
        case 2: search()
        case 3: download()

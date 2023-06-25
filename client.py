import socket
import json
import os

# Creation of a socket object
socket_server = socket.socket()
socket_peer = socket.socket()

# Define port to connect with server
PORT = 1099

def join():
    """ Join """
    peer_ip = input("Digite o ip: ")
    peer_port = int(input("Digite a porta: "))
    peer_address = f"{peer_ip}:{peer_port}"
    folder_path = str(input(("Digite o nome da pasta com os arquivos: ")))
    filenames = get_filenames(folder_path)
    message_to_server = {"type": "JOIN", "address": peer_address, "filenames": filenames}
    server_message = connect_to_server(message_to_server)
    if server_message == "JOIN_OK":
        print(f'Sou peer {peer_address} com arquivos {filenames}')
    socket_server.close()

def search():
    """ Search """
    filename = str(input(("Digite o nome do arquivo que está procurando: ")))
    peer_addresses = connect_to_server({"type": "SEARCH", "filename": filename})
    print(f'peers com arquivo solicitado: {json.loads(peer_addresses)}')
    socket_server.close()

def download():
    """ Download """
    peer_address = (input("Digite o ip: "), int(input("Digite a porta: ")))
    filename = str(input(("Digite o nome do arquivo para download: ")))
    connect_to_server({"type": "DOWNLOAD", "address": peer_address, "filename": filename})
    socket_server.close()

def connect_to_server(message_to_server: dict):
    """ Connect """
    socket_server.connect(('', PORT))
    socket_server.sendall(json.dumps(message_to_server).encode())
    return socket_server.recv(1024).decode()

def get_filenames(folder_path: str):
    """ Get filenames """
    filenames = []
    for filename in os.listdir(folder_path):
        filenames.append(filename)
    return filenames

while True:
    action = int(input('''Escolha uma ação:  
        1 - Join
        2 - Search
        3 - Download
    '''))

    match action:
        case 1: join()
        case 2: search()
        case 3: download()

import socket
import json
import os
from threading import Thread

# Define port to connect with server
PORT = 1099

socket_server = socket.socket()
socket_peer = socket.socket()
socket_download = socket.socket()
folder_path = ""
peer_ip = ""
peer_port = 0

def join():
    """ Join """
    peer_ip = input("Digite o ip: ")
    peer_port = int(input("Digite a porta: "))
    peer_address = f"{peer_ip}:{peer_port}"
    folder_path = str(input(("Digite o nome da pasta com os arquivos: ")))
    filenames = get_filenames()

    socket_server.connect(('', PORT))
    message_to_server = {"type": "JOIN", "address": peer_address, "filenames": filenames}
    server_message = send_message_to_server(socket_server, message_to_server)
    if server_message == "JOIN_OK":
        print(f'Sou peer {peer_address} com arquivos {filenames}')

def search():
    """ Search """
    filename = str(input(("Digite o nome do arquivo que está procurando: ")))
    message_to_server = {"type": "SEARCH", "filename": filename}
    peer_addresses = send_message_to_server(socket_server, message_to_server)
    print(f'peers com arquivo solicitado: {json.loads(peer_addresses)}')

def download():
    """ Download """
    peer_ip = input("Digite o ip: ")
    peer_port = int(input("Digite a porta: "))
    peer_address = f"{peer_ip}:{peer_port}"
    filename = str(input(("Digite o nome do arquivo para download: ")))

    socket_peer.connect(('', peer_port))
    message_to_server = {"type": "DOWNLOAD", "address": peer_address, "filename": filename}
    send_message_to_server(socket_peer, message_to_server)
    print(f'Arquivo {filename} baixado com sucesso na pasta {folder_path}')
    update(filename)

def update(filename: str):
    """ Update """
    message_to_server = {"type": "UPDATE", "filename": filename}
    send_message_to_server(socket_server, message_to_server)

def send_message_to_server(socket: socket, message_to_server: dict):
    """ Connect """    
    socket.sendall(json.dumps(message_to_server).encode())
    return socket.recv(1024).decode()

def get_filenames():
    """ Get filenames """
    filenames = []
    for filename in os.listdir(folder_path):
        filenames.append(filename)
    return filenames

def listen_connections():
    """ Listen """
    while True:
        socket_download.accept()
        thread = Thread(target=process_message)
        thread.start()

def process_message():
    """ Listen """
    while True:
        socket_download.bind(('', peer_port))
        socket_download.listen(5)
        filename = json.loads(socket_download.recv(1024).decode())

        with open(folder_path + filename, "rb") as f:
            bytes_read = f.read()
            socket_download.sendall(bytes_read)

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

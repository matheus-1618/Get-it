import socket
import sys
sys.path.insert(3, ['src','templates','img'])
from pathlib import Path
from src.utils import extract_route, read_file, build_response
from src.views import index
import data.database as database

CUR_DIR = Path(__file__).parent

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
 
    route = extract_route(request)

    db = database.Database("banco")
    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request,db)
    else:
        response = build_response(body='ERRO de Requisição...',code=404)

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()
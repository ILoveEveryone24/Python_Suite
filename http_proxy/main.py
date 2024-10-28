import socket
import sys
import subprocess
import tempfile
import os

def edit_request(request_data):
    request_str = request_data.decode("utf-8")

    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w+", delete=False) as temp_file:
        temp_file.write(request_str)
        temp_file.flush()

        editor = os.getenv("EDITOR", "vim")
        subprocess.call([editor, temp_file.name])

        temp_file.seek(0)
        edited_data = temp_file.read()

    os.unlink(temp_file.name)

    return edited_data

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"[RECEIVED] {request.decode()}")
    target_server_addr = sys.argv[1]
    target_server_port = int(sys.argv[2])

    edit_request(request) 

    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_server_addr, target_server_port))
    target_socket.send(request)

    response = target_socket.recv(4096)
    print(f"[SENDING BACK] {response.decode()}")
    client_socket.send(response)

    client_socket.close()
    target_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(3)
    print(f"[LISTENING] Proxy server listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[CONNECTED] {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server(8080)

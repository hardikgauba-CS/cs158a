import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
BUF_SIZE = 1024

clients = {}

def broadcast(message, sender_sock):
    for client_sock in clients:
        if client_sock != sender_sock:
            try:
                client_sock.send(message.encode())
            except:
                client_sock.close()

def handle_client(client_sock, client_addr):
    print(f"New connection from {client_addr}")
    clients[client_sock] = client_addr[1]

    while True:
        try:
            msg = client_sock.recv(BUF_SIZE).decode()
            if msg.lower() == "exit":
                print(f"Client {client_addr} disconnected.")
                del clients[client_sock]
                client_sock.close()
                break
            full_msg = f"{client_addr[1]}: {msg}"
            print(full_msg)
            broadcast(full_msg, client_sock)
        except:
            if client_sock in clients:
                del clients[client_sock]
            client_sock.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_sock, client_addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        thread.start()

if __name__ == "__main__":
    start_server()

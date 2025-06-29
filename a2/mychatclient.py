import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
BUF_SIZE = 1024

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(BUF_SIZE).decode()
            if data:
                print(data)
        except:
            break                     # connection closed or error → exit thread

def main():
    # 1️⃣ create & connect TCP socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))

    # 2️⃣ **THIS IS THE LINE WITH THE MESSAGE YOU WANT**
    print("Connected to chat server. Type 'exit' to leave.")

    # 3️⃣ start background thread to read incoming messages
    threading.Thread(target=receive_messages,
                     args=(client_sock,),
                     daemon=True).start()

    # 4️⃣ main loop: read keyboard input and send to server
    while True:
        msg = input()
        client_sock.send(msg.encode())
        if msg.lower() == "exit":
            break                    # graceful exit

    client_sock.close()
    print("Disconnected from server")

if __name__ == "__main__":
    main()

import socket

HOST = 'localhost'
PORT = 12345
BUFSIZE = 64

def recv_exact(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(min(BUFSIZE, length - len(data)))
        if not more:
            break
        data += more
    return data

def handle_client(conn, addr):
    print(f"Connected from {addr}")

    # Step 1: Read 2 bytes for message length
    len_bytes = recv_exact(conn, 2)
    if not len_bytes:
        return
    msg_len = int(len_bytes.decode())
    print(f"msg_len: {msg_len}")

    # Step 2: Read exact number of characters
    message = recv_exact(conn, msg_len).decode()
    print(f"processed: {message}")

    # Step 3: Capitalize and send back
    response = message.upper()
    conn.sendall(f"{msg_len:02d}".encode() + response.encode())
    print(f"msg_len_sent: {msg_len}")

    conn.close()
    print("Connection closed\n")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    main()


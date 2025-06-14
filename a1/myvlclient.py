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

def main():
    message = input("Input lowercase sentence: ").strip()
    msg_len = f"{len(message):02d}"
    full_message = msg_len + message

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(full_message.encode())

        # Receive 2-byte length
        len_bytes = recv_exact(s, 2)
        response_len = int(len_bytes.decode())

        # Receive capitalized message
        response = recv_exact(s, response_len).decode()
        print("From Server:", response)

if __name__ == "__main__":
    main()


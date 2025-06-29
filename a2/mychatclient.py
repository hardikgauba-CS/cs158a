import socket, threading

HOST, PORT = "127.0.0.1", 12345
BUF = 1024

def reader(sock):
    buf = ""
    while True:
        try:
            chunk = sock.recv(BUF).decode()
            if not chunk:
                break            # server closed
            buf += chunk
            while "\n" in buf:   # pull complete lines
                line, buf = buf.split("\n", 1)
                if line:
                    print(line)
        except:
            break

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected to chat server. Type 'exit' to leave.")

    threading.Thread(target=reader, args=(s,), daemon=True).start()

    while True:
        msg = input()
        s.send(msg.encode())
        if msg.lower() == "exit":
            break

    s.close()
    print("Disconnected from server")

if __name__ == "__main__":
    main()

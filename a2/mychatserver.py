import socket, threading

HOST, PORT = "127.0.0.1", 12345
BUF = 1024
clients = {}                     # { sock : port }

def broadcast(line: str, sender):
    line += "\n"                 # ← delimiter so clients can split packets
    for s in list(clients):
        if s is sender:          # ← do NOT send back to the originator
            continue
        try:
            s.sendall(line.encode())
        except:
            s.close()
            clients.pop(s, None)

def client_loop(s, addr):
    clients[s] = addr[1]
    print(f"New connection from {addr}")
    try:
        while True:
            data = s.recv(BUF).decode()
            if not data:
                break            # client crashed
            if data.lower() == "exit":
                break
            msg = f"{addr[1]}: {data}"
            print(msg)
            broadcast(msg, s)
    finally:
        s.close()
        clients.pop(s, None)
        print(f"Client {addr} disconnected.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            c, a = srv.accept()
            threading.Thread(target=client_loop, args=(c, a), daemon=True).start()

if __name__ == "__main__":
    main()

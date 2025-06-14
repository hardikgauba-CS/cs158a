# CS158A Assignment 1: Variable-Length TCP Client/Server

## 📌 Description

This project implements a TCP client-server system that exchanges variable-length messages. Each message includes a 2-byte prefix indicating the number of characters in the message.

- The client sends a message prefixed with its 2-digit length (e.g., `10helloworld`).
- The server reads the length, processes that many bytes, converts the message to **uppercase**, and returns it.
- The server stays running, and the client exits after receiving the response.

---

## 🛠 How to Run

### 🖥 Terminal 1: Start the Server

```bash
cd a1
python3 myvlserver.py

we will see something like <img width="562" alt="server_output" src="https://github.com/user-attachments/assets/b780f594-32e3-49f3-80d6-4f31ee594789" />
for Client it will be something like this in terminal
<img width="563" alt="client_output" src="https://github.com/user-attachments/assets/2afcb514-1295-4156-a59e-17c79a2d247f" />

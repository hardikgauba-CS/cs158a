# CS 158A - Assignment 2: Chat Server with Multiple Clients

## 📌 Objective

This project demonstrates a TCP-based multi-client chat application. A central server receives and forwards messages from each client to all other connected clients. The goal is to use sockets and threading to support simultaneous real-time communication.

---

## 📁 Files in This Directory

| File Name         | Description                                      |
|------------------|--------------------------------------------------|
| `mychatserver.py` | The main chat server that accepts multiple clients using TCP sockets and threads. |
| `mychatclient.py` | The client program to connect and communicate with the server. |
| `README.md`       | This documentation with setup instructions and execution examples. |

---

## 🚀 How to Run

### 🖥️ 1. Start the Server

python3 mychatserver.py

### 🖥️ 2. Start the Client

python3 mychatclient.py

### Server
<p align="center"> <img width="800" alt="Server Screenshot" src="https://github.com/user-attachments/assets/6ad57178-3dad-40a0-b312-f5fa4dffa967" /> </p>
### Clients
<table width="100%" style="table-layout: fixed;">
  <tr>
    <td align="center"><strong>Client 1</strong></td>
    <td align="center"><strong>Client 2</strong></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/25e5ebcc-6ff5-414a-b210-1eccc93ecfc7" width="100%"/></td>
    <td><img src="https://github.com/user-attachments/assets/3912892a-94a0-4812-85d5-5055fda1fb47" width="100%"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Client 3</strong></td>
    <td></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/ad7ca6eb-9c41-4866-ab82-bf55967bcf7e" width="100%"/></td>
    <td></td>
  </tr>
</table>

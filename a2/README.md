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

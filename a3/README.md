# 🌀 Leader Election in Asynchronous Ring — CS158A Assignment 3

## 📌 Description
This project implements a **Leader Election Algorithm** in a 
**unidirectional asynchronous ring** using Python sockets and UUIDs. Each 
node runs independently and communicates with its right neighbor to elect 
the node with the **highest UUID** as the leader.

### 🧠 Key Concepts
- Each node has a unique UUID.
- UUIDs are passed clockwise in the ring.
- Nodes forward higher UUIDs and ignore smaller ones.
- If a node receives its own UUID, it declares itself the leader.
- The leader sends a broadcast (`flag=1`) to signal election completion.

---

## 📁 Folder Structure

## 📁 Folder Structure

```
a3/
├── myleprocess.py     # Main Python script
├── config1.txt        # Server & client port for node 1
├── config2.txt        # For node 2
├── config3.txt        # For node 3
├── log1.txt           # Output log for node 1
├── log2.txt           # Output log for node 2
├── log3.txt           # Output log for node 3
└── README.md          # This file
```

## ⚙️ Configuration

Each `configX.txt` file must contain **two lines**:

127.0.0.1,5001 # This node’s server (receive) IP and port
127.0.0.1,5002 # This node’s client (send) neighbor IP and port


Each node must point to its neighbor to form a **closed ring**.

---

## ▶️ How to Run

In **three separate terminals**, run:

```bash
# Terminal 1
python3 -u myleprocess.py config1.txt 1

# Terminal 2
python3 -u myleprocess.py config2.txt 2

# Terminal 3
python3 -u myleprocess.py config3.txt 3
Log files will be written as log1.txt, log2.txt, etc.

📝 Sample Log Output

23:24:10 Connection refused by 127.0.0.1:5002 — retrying in 5s
23:24:25 Connected to server at 127.0.0.1:5002
23:24:25 Sent: uuid=5b129123-6a66-4c66-99e7-d9ea7da6f5ee, flag=0
23:24:34 Received: uuid=548fd34b..., flag=0, less, 0
23:24:34 Ignored message: uuid=548fd34b..., flag=0
23:24:37 Received: uuid=5b129123..., flag=0, same, 0
23:24:37 Leader elected → 5b129123...
23:24:37 Sent: uuid=5b129123..., flag=1
23:24:47 Terminating after convergence (idle 10.5s)
✅ Output Verification

✅ Leader elected by only 1 node
✅ All nodes agree on same leader UUID
✅ Termination condition met after flag=1
🧑‍💻 Requirements

Python 3.x
Standard libraries only: uuid, socket, asyncio, threading, queue, json, 
sys, time, logging, pathlib
🏁 Final Output

On successful execution, every node prints:

leader is <UUID>

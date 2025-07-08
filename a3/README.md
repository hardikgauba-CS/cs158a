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

Each `config.txt` file must contain **two lines**:

```txt
127.0.0.1,5001  # This node’s server (receive) IP and port  
127.0.0.1,5002  # This node’s client (send) neighbor IP and port
```


Each node must point to its neighbor to form a **closed ring**.

---

## ▶️ How to Run

In **three separate terminals**, run:

```bash
# Terminal 1
python3 -u myleprocess.py config1.txt 

# Terminal 2
python3 -u myleprocess.py config2.txt

# Terminal 3
python3 -u myleprocess.py config3.txt
Log files will be written as log1.txt, log2.txt, etc.
```
📝 Log Output for log1.txt

<img width="978" alt="Screenshot 2025-07-08 at 11 40 39 AM" src="https://github.com/user-attachments/assets/b3ffc1b6-9da9-4d73-ad03-f955bddb9d70" />

📝 Log Output for log2.txt

<img width="681" alt="Screenshot 2025-07-08 at 11 40 50 AM" src="https://github.com/user-attachments/assets/f8bdd49f-21b0-44a1-986c-1c4a0f29b320" />

📝 Log Output for log3.txt

<img width="681" alt="Screenshot 2025-07-08 at 11 41 03 AM" src="https://github.com/user-attachments/assets/60f554f7-07ec-433e-9732-727113f4a12f" />

### ✅ Output Verification  
✅ Leader elected by only 1 node  
✅ All nodes agree on same leader UUID  
✅ Termination condition met after flag=1  

### 🧑‍💻 Requirements  
- Python 3.x  
- Standard libraries only:  
  `uuid`, `socket`, `asyncio`, `threading`, `queue`, `json`, `sys`, `time`, `logging`, `pathlib`  

### 🏁 Final Output  
<img width="1456" alt="Screenshot 2025-07-08 at 11 52 50 AM" src="https://github.com/user-attachments/assets/653f135c-1ffc-41eb-b3a5-b517f782900e" />

On successful execution, every node prints:

leader is 5b129123-6a66-4c66-99e7-d9ea7da6f5ee

from __future__ import annotations

import asyncio
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Tuple

MESSAGE_END = "\n"  # newline terminates every JSON message

class Message:
    """Lightweight wrapper for the JSON wire‑format used in the ring."""

    def __init__(self, node_id: uuid.UUID, flag: int = 0):
        self.uuid: uuid.UUID = node_id
        self.flag: int = flag  # 0 ⇒ election phase, 1 ⇒ leader announced

    def to_wire(self) -> bytes:
        return (json.dumps({'uuid': str(self.uuid), 'flag': self.flag}) + MESSAGE_END).encode()

    @classmethod
    def from_wire(cls, raw: str) -> "Message":
        data = json.loads(raw)
        return cls(uuid.UUID(data['uuid']), int(data['flag']))

    def is_election(self) -> bool:            # helper
        return self.flag == 0

    def is_leader_announcement(self) -> bool: # helper
        return self.flag == 1

class Node:
    """A single participant in the asynchronous non‑anonymous ring."""

    def __init__(self, cfg_path: Path, node_index: int | None = None):
        self.server_ip, self.server_port, self.client_ip, self.client_port = self._parse_cfg(cfg_path)
        self.uuid: uuid.UUID = uuid.uuid4()
        self.leader_id: uuid.UUID | None = None
        self.state: int = 0  # 0 ⇒ election in progress, 1 ⇒ leader known

        # async primitives
        self.outgoing: asyncio.Queue[Message] = asyncio.Queue()
        self.client_writer: asyncio.StreamWriter | None = None
        self._leader_forwarded: bool = False
        self._last_activity: float = time.time()

        # initialise logger
        self._logger = self._init_logger(node_index)

    def _init_logger(self, node_index: int | None):
        import logging, os

        if node_index in (1, 2, 3):
            log_name = f"log{node_index}.txt"
        else:
            picked = None
            for i in (1, 2, 3):
                fname = f"log{i}.txt"
                try:
                    fd = os.open(fname, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
                    os.close(fd)
                    picked = fname
                    break
                except FileExistsError:
                    continue
            log_name = picked or f"log_{str(self.uuid)[:8]}.txt"

        logger = logging.getLogger(str(self.uuid))
        logger.setLevel(logging.INFO)
        logger.propagate = False

        fmt = logging.Formatter("%(asctime)s %(message)s", datefmt="%H:%M:%S")

        f_handler = logging.FileHandler(log_name, mode="a", encoding="utf-8")
        f_handler.setFormatter(fmt)
        logger.addHandler(f_handler)

        s_handler = logging.StreamHandler(sys.stdout)
        s_handler.setFormatter(fmt)
        logger.addHandler(s_handler)

        return logger

    @staticmethod
    def _parse_cfg(cfg_path: Path) -> Tuple[str, int, str, int]:
        lines = [ln.strip() for ln in cfg_path.read_text().splitlines() if ln.strip()]
        if len(lines) < 2:
            raise RuntimeError("Config file must contain two non‑blank lines (server, client).")
        srv_ip, srv_port = lines[0].split(',')
        cli_ip, cli_port = lines[1].split(',')
        return srv_ip, int(srv_port), cli_ip, int(cli_port)

    async def run(self):
        self._logger.info("Process UUID = %s", self.uuid)
        server = await asyncio.start_server(self._handle_server, self.server_ip, self.server_port)
        self._logger.info("Server listening on %s:%s", self.server_ip, self.server_port)
        async with server:
            await asyncio.gather(server.serve_forever(), self._client_loop(), self._watchdog())

    async def _handle_server(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._logger.info("Accepted connection from %s", writer.get_extra_info('peername'))
        try:
            while True:
                raw = await reader.readline()
                if not raw:
                    break
                msg = Message.from_wire(raw.decode())
                cmp_state = "greater" if msg.uuid > self.uuid else ("less" if msg.uuid < self.uuid else "same")
                leader_info = f", leader_id={self.leader_id}" if self.state == 1 else ""
                self._logger.info("Received: uuid=%s, flag=%d, %s, %d%s", msg.uuid, msg.flag, cmp_state, self.state, leader_info)
                self._last_activity = time.time()
                await self._process_message(msg)
        finally:
            writer.close()
            await writer.wait_closed()

    async def _client_loop(self):
        while self.client_writer is None:
            try:
                reader, writer = await asyncio.open_connection(self.client_ip, self.client_port)
                self.client_writer = writer
                self._logger.info("Connected to server at %s:%s", self.client_ip, self.client_port)
            except (ConnectionRefusedError, OSError):
                self._logger.info("Connection refused by %s:%s — retrying in 5s", self.client_ip, self.client_port)
                await asyncio.sleep(5)

        await self._send(Message(self.uuid, 0))

        while True:
            msg = await self.outgoing.get()
            await self._send(msg)
            if msg.is_leader_announcement():
                self._leader_forwarded = True

    async def _send(self, msg: Message):
        assert self.client_writer is not None, "Client writer not ready"
        self.client_writer.write(msg.to_wire())
        await self.client_writer.drain()
        self._logger.info("Sent: uuid=%s, flag=%d", msg.uuid, msg.flag)
        self._last_activity = time.time()

    async def _process_message(self, msg: Message):
        if msg.is_election():
            if msg.uuid == self.uuid:
                self.leader_id, self.state = self.uuid, 1
                self._logger.info("Leader elected → %s", self.leader_id)
                await self.outgoing.put(Message(self.leader_id, 1))
            elif msg.uuid > self.uuid:
                await self.outgoing.put(msg)
            else:
                self._logger.info("Ignored message: uuid=%s, flag=%d", msg.uuid, msg.flag)
        else:
            if self.state == 0:
                self.leader_id, self.state = msg.uuid, 1
                self._logger.info("Acknowledged leader → %s", self.leader_id)
            if not self._leader_forwarded:
                await self.outgoing.put(msg)

    async def _watchdog(self):
        while True:
            await asyncio.sleep(2)
            idle = time.time() - self._last_activity
            if self.state == 1 and self._leader_forwarded and idle > 10:
                self._logger.info("Terminating after convergence (idle %.1fs)", idle)
                print(f"leader is {self.leader_id}")
                for t in asyncio.all_tasks():
                    if t is not asyncio.current_task():
                        t.cancel()
                break

def main():
    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config.txt")
    index = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
    node = Node(cfg_path, index)
    try:
        asyncio.run(node.run())
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    main()
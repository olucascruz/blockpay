from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import time
from typing import List
import json
import os
import socket
import uvicorn
import requests


PORT = 8000

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start app
    ip = get_local_ip()
    server_with_port = f"http://{ip}:{PORT}"
    response = requests.post("http://127.0.0.1:8001/ip", json={"ip":server_with_port})
    print(response.content)
    yield
    # Finish app
    
app = FastAPI(lifespan=lifespan, title="API de Blockchain para Registro de Pagamentos")

# Classe para o Bloco
class Block:
    def __init__(self, index: int, timestamp: float, data: dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        raw = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        prefix = "0" * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

# Classe para a Blockchain
class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.load_from_file()
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, time.time(), {"mensagem": "Bloco Gênesis"}, "0")
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: dict):
        last_block = self.get_last_block()
        new_block = Block(len(self.chain), time.time(), data, last_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_to_file()

    def get_all_data(self):
        return [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }
            for block in self.chain
        ]
    
    def save_to_file(self, filename="blockchain.json"):
        data = [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
                "nonce": block.nonce
            }
            for block in self.chain
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="blockchain.json"):
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.chain = []
                for entry in data:
                    block = Block(
                        index=entry["index"],
                        timestamp=entry["timestamp"],
                        data=entry["data"],
                        previous_hash=entry["previous_hash"]
                    )
                    block.hash = entry["hash"]
                    block.nonce = entry["nonce"]
                    self.chain.append(block)


# Inicializa a blockchain
blockchain = Blockchain()

# Modelo dos dados de pagamento
class Pagamento(BaseModel):
    descricao: str
    preco: float
    pagante: str





# Rota de registro
@app.post("/registrar_pagamento")
def registrar_pagamento(pagamento: Pagamento):
    blockchain.add_block(pagamento.dict())
    return {"mensagem": "Pagamento registrado com sucesso!"}

# Rota para listar
@app.get("/listar_pagamentos")
def listar_pagamentos():
    return {"blockchain": blockchain.get_all_data()}

# Rota para buscar pagamentos de um só pagante especifico
@app.get("/buscar_pagamentos/{pagante}")
def buscar_pagamentos(pagante: str):
    resultados = []
    for block in blockchain.chain:
        data = block.data
        if isinstance(data, dict) and data.get("pagante") == pagante:
            resultados.append({
                "descricao": data["descricao"],
                "preco": data["preco"],
                "bloco": block.index,
                "hash": block.hash
            })
    return {"pagamentos_do_pagante": resultados}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
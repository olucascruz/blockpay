from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

import socket
import uvicorn
import requests
from fastapi import Body
from typing import Any
import random
from Block import Block
PORT = 8000
from Blockchain import Blockchain

SERVER_AUX = "http://127.0.0.1:8001"
# Inicializa a blockchain
blockchain = Blockchain()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start app
    ip = get_local_ip()
    server_with_port = f"http://{ip}:{PORT}"
    response = requests.post(f"{SERVER_AUX}/ip", json={"ip":server_with_port})
    response = requests.get(f"{SERVER_AUX}/ip")
    list_ips = response.json()["ips"]

    chain = sync_from_random_peer(list_ips)
    blockchain.import_chain(chain)
    yield
    # Finish app
    
app = FastAPI(lifespan=lifespan, title="API de Blockchain para Registro de Pagamentos")

# Modelo dos dados de pagamento
class Pagamento(BaseModel):
    descricao: str
    preco: float
    pagante: str

# Rota de registro
@app.post("/registrar_pagamento")
def registrar_pagamento(pagamento: Pagamento):
    new_block = blockchain.create_block(pagamento.dict())
    blockchain.insert_block(new_block)
    response = requests.get(f"{SERVER_AUX}/ip")
    list_ips = response.json()["ips"]
    for ip in list_ips:
        if get_local_ip() not in ip:
            try:
                response = requests.post(f"{ip}/atualizar_pagamento", json=new_block.get_data())
            except Exception as ex:
                print(ex)
    return {"mensagem": "Pagamento registrado com sucesso!"}


class BlockModel(BaseModel):
    index: int
    timestamp: str
    data: Any
    hash: str
    previous_hash: str

@app.post("/atualizar_pagamento")
def atualizar_pagamento(new_block: dict= Body(...)):
      new_block = Block(**new_block)
      blockchain.insert_block(new_block)
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

def sync_from_random_peer(peers: list) -> list | None:
    random.shuffle(peers)
    for peer in peers:
        if get_local_ip() in peer: continue
        try:
            response = requests.get(f"{peer}/export")
            if response.status_code == 200:
                chain_data = response.json()
                return chain_data
        except:
            continue
    return None

@app.get("/hello")
def hello():
    return {"hello":"hello"}     



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
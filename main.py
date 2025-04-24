from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime
import socket
import uvicorn
import requests
from fastapi import Body
from typing import Any, Optional, List
import random
from Block import Block
from Blockchain import Blockchain
from fastapi.middleware.cors import CORSMiddleware
from security import get_password_hash, authenticate_user
from copy import deepcopy
import random
import string

PORT = 8000

SERVER_AUX = "http://192.168.1.10:8001"
# Inicializa a blockchain
blockchain = Blockchain()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # # Start app
    # ip = get_local_ip()
    # server_with_port = f"http://{ip}:{PORT}"
    # response = requests.post(f"{SERVER_AUX}/ip", json={"ip":server_with_port})
    # response = requests.get(f"{SERVER_AUX}/ip")
    # list_ips = response.json()["ips"]

    # chain = sync_from_random_peer(list_ips)
    # if chain != None:
    #     blockchain.import_chain(chain)
    yield
    # Finish app
    
app = FastAPI(lifespan=lifespan, title="API de Blockchain para Registro de Pagamentos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo dos dados de pagamento
class Pagamento(BaseModel):
    id: UUID
    id_usuario: str
    nome: str
    descricao: str
    preco: float
    tipo: str
    data: datetime
    base64: Optional[str] = None
    valida: bool

# Rota de registro
@app.post("/registrar_pagamento")
def registrar_pagamento(pagamento: Pagamento):
    pagamento = pagamento.model_dump()
    pagamento["id"] = str(pagamento["id"])
    pagamento["data"] = str(pagamento["data"])
    pagamento["block_type"] = "transaction"
    new_block = blockchain.create_block(pagamento)
    blockchain.insert_block(new_block)
    
    return {"mensagem": "Pagamento registrado com sucesso!"}


def sync_peers(new_block:Block):
    response = requests.get(f"{SERVER_AUX}/ip")
    list_ips = response.json()["ips"]
    for ip in list_ips:
        if get_local_ip() not in ip:
            try:
                response = requests.post(f"{ip}//atualizar_blockchain", json=new_block.get_data())
            except Exception as ex:
                print(ex)


class Group(BaseModel):
    criador: str
    participantes:List[str]

def gerar_codigo_grupo(tamanho=6):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

@app.post("/group")
def create_group(group:Group):
    """
    Create group users
    """
    group = group.model_dump()
    group["id"] = gerar_codigo_grupo(6)
    group["block_type"] = "group"


    new_block = blockchain.create_block(group)
    blockchain.insert_block(new_block)
    sync_peers(new_block)
    
    return {"mensagem": "Grupo criado!"}



class User(BaseModel):
    nome: str
    email: str
    senha: str


@app.post("/register")
def register_user(user:User):
    """
    Register user
    """
    user = user.model_dump()

    list_users = blockchain.get_data_by_type("user")
    for user_in_list in list_users:
        if user["email"] == user_in_list["data"]["email"]:
            raise HTTPException(status_code=409, detail="Usuário não encontrado")

    user["id"] = str(uuid4())
    user["block_type"] = "user"
    user["senha"] = get_password_hash(user["senha"])

    new_block = blockchain.create_block(user)
    blockchain.insert_block(new_block)
    sync_peers(new_block)
    
    return {"mensagem": "usuário criado criado!"}

class UserLogin(BaseModel):
    email: str
    senha: str

class UserPublic(BaseModel):
    id:str
    email: str
    nome: str

@app.post("/login", response_model=UserPublic)
def login_user(user:UserLogin):
    list_users = blockchain.get_data_by_type("user")
    user = user.model_dump()
    user = authenticate_user(list_users=list_users, username=user["email"], password=user["senha"])

    if user: return user["data"]
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/user", response_model=UserPublic)
def get_user_by_id(id:str):
    users = blockchain.get_data_by_type("user")

    print(id)
    for user in users:
        if user["data"].get("id") == id:
            return user["data"]
        
    raise HTTPException(status_code=404, detail="usuário não encontrado")

class DataEnterGroup(BaseModel):
    user_id:str
    code_group: str


@app.post("/group/enter")
def enter_in_group(data_enter_group: DataEnterGroup):
    user_id = data_enter_group.user_id
    code_group = data_enter_group.code_group

    groups = blockchain.get_data_by_type("group")

    groups_searched = []
    for group in groups:
        if group["data"]["id"] == code_group:
            groups_searched.append(group)
    
    
    if len(groups_searched) < 1:    
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    group = max(groups_searched, key=lambda x: x["timestamp"])
    if user_id not in group["data"]["participantes"]:
        group["data"]["participantes"].append(user_id)
    
    new_version_group = blockchain.create_block(group["data"])
    blockchain.insert_block(new_version_group)
    return {"mensagem": "entrou no grupo!"}


@app.get("/group")
def get_group_by_user(user_id:str):
    groups = blockchain.get_data_by_type("group")

    list_groups_with_user = []
    for group in groups:
        data_group = group["data"] 
        if user_id in data_group["participantes"]:
            list_groups_with_user.append(group)
    

    if len(list_groups_with_user) < 1:    
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    group = max(list_groups_with_user, key=lambda x: x["timestamp"])
    return group["data"]

class BlockModel(BaseModel):
    index: int
    timestamp: str
    data: Any
    hash: str
    previous_hash: str

@app.post("/atualizar_blockchain")
def atualizar_pagamento(new_block: dict= Body(...)):
      new_block = Block(**new_block)
      blockchain.insert_block(new_block)
      return {"mensagem": "Pagamento registrado com sucesso!"}

# Rota para listar
@app.get("/listar_pagamentos")
def listar_pagamentos():
    return {"blockchain": blockchain.get_all_data()}

# Rota para buscar pagamentos de um só pagante especifico
@app.get("/pagamento")
def buscar_pagamentos(id_usuario: str):
    resultados = []
    for block in blockchain.chain:
        data = block.data
        if isinstance(data, dict) and data.get("id_usuario") == id_usuario:
            info = deepcopy(data)
            resultados.append(info)

    if len(resultados) < 1:
        raise HTTPException(status_code=404, detail="Transferencias não encontradas")
    
    return resultados



@app.get("/export")
def export_blockchain_data():
    return blockchain.get_all_data()

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
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Any, Optional, List



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
    
    
class Group(BaseModel):
    criador: str
    participantes:List[str]


class User(BaseModel):
    nome: str
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

class UserPublic(BaseModel):
    id:str
    email: str
    nome: str

class DataEnterGroup(BaseModel):
    user_id:str
    code_group: str

class BlockModel(BaseModel):
    index: int
    timestamp: str
    data: Any
    hash: str
    previous_hash: str
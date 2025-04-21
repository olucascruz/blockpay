from fastapi import FastAPI
import json
from typing import List
import os
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Server auxiliar ips")


CAMINHO_ARQUIVO = "ips.json"
PORT = 8001

def load_ips() -> List[str]:
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ips(ips: List[str]):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(ips, f, ensure_ascii=False, indent=4)


@app.get("/hello")
def hello():
    return {"hello":"hello"}     


class IPModel(BaseModel):
    ip: str

@app.post("/ip")
def insert_ip(ip:IPModel):
    ip = ip.ip
    ips = load_ips()
    if ip not in ips:
        ips.append(ip)
        save_ips(ips)
    return {"mensagem": "IP inserido com sucesso", "ip": ip}
        

@app.get("/ip")
def get_ips():
    ips = load_ips()
    return {"ips": ips}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
import socket
import random
import requests
from Block import Block

SERVER_AUX = "http://192.168.1.10:8001"

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

def sync_peers(new_block:Block):
    response = requests.get(f"{SERVER_AUX}/ip")
    list_ips = response.json()["ips"]
    for ip in list_ips:
        if get_local_ip() not in ip:
            try:
                response = requests.post(f"{ip}/atualizar_blockchain", json=new_block.get_data())
            except Exception as ex:
                print(ex)

def gerar_codigo_grupo(tamanho=6):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))

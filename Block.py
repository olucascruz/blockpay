import hashlib

# Classe para o Bloco
class Block:
    def __init__(self, index: int, timestamp: float, data: dict, previous_hash: str, hash:str=None, nonce:int=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        if hash != None:
            self.hash = hash
        else:
            self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        raw = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        prefix = "0" * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

     
    def get_data(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }

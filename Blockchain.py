import time
from typing import List
import json
import os
from Block import Block

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

    def insert_block(self, new_block):
        self.chain.append(new_block)
        if self.is_blockchain_valid():
            self.save_to_file()

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def create_block(self, data: dict):
        last_block = self.get_last_block()
        new_block = Block(len(self.chain), time.time(), data, last_block.hash)
        new_block.mine_block(self.difficulty)
        return new_block
   

    def get_all_data(self):
        return [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "hash": block.hash,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce
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

    def import_chain(self, received_chain: list) -> bool:
        new_chain = []
        for entry in received_chain:
            block = Block(
                        index=entry["index"],
                        timestamp=entry["timestamp"],
                        data=entry["data"],
                        previous_hash=entry["previous_hash"]
                    )
            block.hash = entry["hash"]
            block.nonce = entry["nonce"]
            new_chain.append(block)

        self.chain = new_chain
        if self.is_blockchain_valid():
            self.save_to_file()


    def is_first_block_valid(self):
        """
        Verifica se o bloco gênesis é válido
        """
        first_block = self.blocks[0]
        return (first_block.index == 0 and
                first_block.previous_hash is None and
                first_block.hash == first_block.calculate_hash())
    
    def is_valid_new_block(self, new_block, previous_block):
        """
        Valida um novo bloco com base no bloco anterior
        """
        return (new_block and previous_block and
                previous_block.index + 1 == new_block.index and
                new_block.previous_hash == previous_block.hash and
                new_block.hash == new_block.calculate_hash())
    
    def is_blockchain_valid(self):
        """
        Verifica a integridade da blockchain
        """
        if not self.is_first_block_valid():
            return False
        
        #//Percorre todos os blocos da blockchain
        #//verifica cada bloco em relação ao seu antecessor.
        #//Isso confirma que a blockchain inteira não foi adulterada.
        for i in range(1, len(self.blocks)):
            if not self.is_valid_new_block(self.blocks[i], self.blocks[i-1]):
                return False
        
        return True

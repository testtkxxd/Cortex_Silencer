import hashlib as hasher
from Crypto.Hash import SHA256
import datetime as date
from CVM import CVM
import json
class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.hash_block()

    def hash_block(self):
        sha = SHA256.new((str(self.index) +
        str(self.timestamp) +
        str(self.data) +
        str(self.previous_hash) +
        str(self.nonce)).encode())
        return sha.hexdigest()
    def __dict__(self):
        return {
            "index":self.index,
            "previous_hash":self.previous_hash,
            "timestamp":self.timestamp,
            "data":self.data,
            "nonce":self.nonce,
            "hash":self.hash
        }

class Blockchain(object):
    def __init__(self):
        self._chain = [self.create_genesis_block()]
        self.CVM = CVM()
    # ...blockchain  
    def create_genesis_block(self):
        # Manually construct a block with
        # index zero and arbitrary previous hash
        return Block(
                index =0, 
                timestamp = date.datetime.now(), 
                data = json.dumps([]), 
                previous_hash = "0",
                nonce = 0)
    def add_block(self,data):
        last_block = self._chain[-1]
        new_index = self._chain[-1].index+1
        new_timestamp = date.datetime.now()
        previous_hash = last_block.hash
        header = str(new_index) + str(new_timestamp) + str(data) + str(previous_hash)
        hash_result,nonce = self.proof_of_work(header)
        self._chain.append(
            Block(
                index = new_index, 
                timestamp = new_timestamp, 
                data = data, 
                previous_hash = previous_hash,
                nonce = nonce)
        )
        return self._chain[-1]
    def pack(self,unpaced_transactions, miner_address):
        temp_tx = unpaced_transactions.copy().append({"type":"coinbase_tx","miner_address":miner_address})
        new_state, err = self.CVM.verify(temp_tx)
        if err:
            return None,err
        return self.add_block(json.dumps(temp_tx)),None        

    def proof_of_work(self,header):
        target = 2**255
        nonce = 0
        while True:
            hash_result = SHA256.new(data=(str(header)+str(nonce)).encode()).hexdigest()
            if int(hash_result,16)<target:
                return hash_result, nonce
            nonce+=1
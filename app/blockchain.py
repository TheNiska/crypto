from hashlib import sha256
from funcs import verify
from controller import get_public_key, add_block


class DataRow:
    def __init__(self, sender: str, recipient: str,
                 amount: float, signature: str):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature  # signature in hex

    def get_transaction_str(self) -> str:
        data = [
            str(self.sender),
            str(self.amount),
            str(self.recipient),
        ]
        return ";".join(data)

    def verify_signature(self) -> bool:
        '''Getting the sender's public key from db and verifying that it's him
        who signed this transaction'''

        public_key = get_public_key(self.sender, db_path="users.db")
        return verify(self.signature, public_key, self.get_transaction_str())

    def __repr__(self):
        return f"({self.sender} sent {self.amount} to {self.recipient})"


class Block:
    def __init__(self, data_rows=None, prev_hash=None):
        self.prev_hash = prev_hash if prev_hash is not None else '0' * 64
        self.num = 1
        self.nonce = 0
        self.hash = None

        self.data = ''
        if data_rows is not None:
            for row in data_rows:
                self.data += f"{row.get_transaction_str()};{row.signature}\n"

        self.mine_hash()

    def get_hash(self) -> str:
        hash_str = f"{self.num}\n{self.nonce}\n{self.data}{self.prev_hash}"
        return sha256((hash_str.encode('utf-8'))).hexdigest()

    def mine_hash(self) -> None:
        VALID_PREFIX = 'ffff'
        current_hash = ''

        while not current_hash.startswith(VALID_PREFIX):
            self.nonce += 1
            current_hash = self.get_hash()

        self.hash = current_hash

    def __repr__(self):
        return f"Hash: {self.hash}\nNonce: {self.nonce}\nData: {self.data}\n" \
               f"Prev_Hash: {self.prev_hash}"


if __name__ == '__main__':

    request = {
        'sender': 'TheNiska',
        'recipient': 'Max',
        'amount': 45,
        'signature': '33f5e2f4b01ae99a446c9e17a0a2942de8d5b9820438569df08cd963'
        '71bdb91d8b1784bb6328e7198a69b71994e7615adda858ff6736fc2adaa0455459d83'
        '3f0ce27f89d94c11f17525d3f129a00d454851f903678bd55d280724440bab394cdd0'
        '6b45f4b6c6f1499abae75b29d0fd7c0a50309053f444e7c61be5db0785edb8f62818f'
        'f7f9692d9593a78534cfb6670b7cae0255a44792c74052442fb29a6d7532ccc13ca3a'
        'a8c9ffef65d0f35fda6de26dfa8ddd8ae2899727b83ff9c772ccbd5f080ce5513806e'
        '32e8e29128c14bd135cc21758b04857445254cd331a1262d27d702d018ca8a53c440f'
        '151a697d93bca37f4adf07baf5956e1762f2d07f3f'
    }

    row1 = DataRow(**request)
    is_valid = row1.verify_signature()
    if is_valid:
        block = Block(data_rows=[row1])
        add_block(block, db_path="blockchain.db")
        
    else:
        print('Validation failed!')

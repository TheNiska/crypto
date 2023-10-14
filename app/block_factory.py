from blockchain import DataRow, Block
from controller import execute_query


class BlockMiner:
    def __init__(self, table_name: str):
        self.db_name = "blockchain.db"
        self.table_name = table_name

    def generate_new_block(self, data_rows: list[DataRow]) -> Block:
        valid_rows = []
        for row in data_rows:
            is_valid = row.verify_signature()
            if is_valid:
                valid_rows.append(row)

        query = f"select max(id) from {self.table_name}"
        prev_num = execute_query(query, db_path=self.db_name)[0][0]
        curr_num = prev_num + 1

        query = f"select hash from {self.table_name} where id='{prev_num}'"
        prev_hash = execute_query(query, db_path=self.db_name)[0][0]

        block = Block(num=curr_num, prev_hash=prev_hash, data_rows=valid_rows)
        return block


miner = BlockMiner('blockchain1')
miner.generate_new_block([])

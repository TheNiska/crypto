from sqlite3 import connect
from hashlib import sha256
try:
    from app.funcs import create_new_pair
except Exception:
    from funcs import create_new_pair


def manage_connection(func):
    def wrapper(*args, db_path=None, **kwargs):
        if db_path is None:
            raise NameError("Required keyword argument 'db_path' is not found")
        con = connect(db_path)
        cur = con.cursor()
        result = None

        try:
            result = func(*args, **kwargs, cur=cur)
            con.commit()
        except Exception as ex:
            print(type(ex).__name__, ': ', ex, sep='')
        else:
            print('Successfully done with database!')
        finally:
            con.close()

        return result
    return wrapper


@manage_connection
def execute_query(query: str, cur=None):
    array = [el for el in cur.execute(query)]
    return array


@manage_connection
def register_user(username: str, password: str, cur=None) -> None:
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    private_key, public_key = create_new_pair(password)

    fields = "(username, password_hash, private_key, public_key)"
    values = f"('{username}', '{hashed_password}', " \
             f"'{private_key}', '{public_key}')"

    query = f"insert into users {fields} values {values}"
    cur.execute(query)


@manage_connection
def get_private_key(username: str, cur=None) -> str:
    '''Returns encrypted private key by username in 'str' format'''

    query = f"select private_key from users where username='{username}'"
    return cur.execute(query).fetchone()[0]


@manage_connection
def get_public_key(username: str, cur=None) -> str:
    '''Returns public key by username in 'str' format'''

    query = f"select public_key from users where username='{username}'"
    return cur.execute(query).fetchone()[0]


@manage_connection
def add_block(block, cur=None):
    fields = "(hash, prev_hash, nonce, data)"
    values = f"('{block.hash}', '{block.prev_hash}', " \
             f"'{block.nonce}', '{block.data}')"

    query = f"insert into blockchain1 {fields} values {values}"
    cur.execute(query)


@manage_connection
def get_blocks(cur=None):
    res = cur.execute("select * from blockchain1").fetchall()
    return res


if __name__ == '__main__':
    query = "select max(id) from blockchain1"
    result = execute_query(query, db_path='blockchain.db')
    print(result)

from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from hashlib import sha256
from funcs import create_new_pair

engine = create_engine("sqlite:///users.db")
conn = engine.connect()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(70), index=True, unique=True)
    password_hash = Column(String(64))
    private_key = Column(String(2000))
    public_key = Column(String(500))


Base.metadata.create_all(bind=engine)


def register_user(username: str, password: str) -> None:
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    private_key, public_key = create_new_pair(password)
    print(len(private_key))
    print(len(public_key))

    user = User(
        username=username,
        password_hash=hashed_password,
        private_key=private_key,
        public_key=public_key
    )

    with Session(autoflush=False, bind=engine) as db:
        db.add(user)
        db.commit()


def get_private_key(username: str) -> str:
    '''Returns encrypted private key by username in 'str' format'''

    query = text(f"select private_key from users where username='{username}'")
    return conn.execute(query).first().private_key


def get_public_key(username: str) -> str:
    '''Returns public key by username in 'str' format'''

    query = text(f"select public_key from users where username='{username}'")
    return conn.execute(query).first().public_key


# register_user('TheNiska', '2012')
# register_user('Dude', '00')
# register_user('July', '1234')

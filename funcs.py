from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


def create_new_pair(password: str) -> (str, str):
    password = password.encode()

    # creating new pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )

    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return (private_key_pem.decode(), public_key_pem.decode())


def sign(data, priv_key_pem, password):
    private_key = serialization.load_pem_private_key(
        priv_key_pem.encode(),
        password=password.encode(),
        backend=default_backend()
    )

    data_to_sign = data.encode()

    signature = private_key.sign(
        data_to_sign,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


def verify(signature, pub_key_pem, data) -> bool:
    public_key = serialization.load_pem_public_key(
        pub_key_pem.encode(),
        backend=default_backend()
    )

    try:
        public_key.verify(
            signature,
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


if __name__ == '__main__':
    priv, pub = create_new_pair('Denis')
    signature = sign('My data', priv, 'Denis')
    print(len(signature.hex()))
    is_valid = verify(signature, pub, 'My data')
    print(is_valid)

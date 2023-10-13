from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


def create_new_pair(password: str) -> (str, str):
    '''Creates private/public keys pair. Encrypts private key with password.
    Returns (private_key, public_key) is string format'''

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


def sign(data: str, priv_key_pem: str, password: str) -> str:
    '''Signs data with encyptes private key. Return signature in hex'''

    private_key = serialization.load_pem_private_key(
        priv_key_pem.encode(),
        password=password.encode(),
        backend=default_backend()
    )

    signature = private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature.hex()


def verify(signature: str, pub_key_pem: str, data: str) -> bool:
    '''Verifies that the given signature if valid for the give public key'''

    bytes_signature = bytes.fromhex(signature)  # from hex to bytes

    public_key = serialization.load_pem_public_key(
        pub_key_pem.encode(),
        backend=default_backend()
    )

    try:
        public_key.verify(
            bytes_signature,
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
    private_key, public_key = create_new_pair('Denis')
    print(f"Private key: {type(private_key)}, public_key: {type(public_key)}")

    signature = sign('Sending money', private_key, 'Denis')
    print("Singature type: ", type(signature))
    print(signature)

    res = verify(signature, public_key, 'Sendng money')
    print(res)
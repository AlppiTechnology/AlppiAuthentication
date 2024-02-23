import jwt, logging
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger('django')
algorithm = 'RS256'


def create_jwt_pass(data) -> str:
    logger.debug('Criando Token JWT')
    private_rsa = read_rsa_pass()

    private_key = serialization.load_ssh_private_key(
    private_rsa, password=b''
    )
    
    encoded = jwt.encode(payload=data, key=private_key, algorithm=algorithm)
    return encoded
    # return encoded.decode('utf-8') antiga lib precisava decodar


def decrypt_jwt_pass(jwt_encoded) -> dict:
    pulic_rsa = read_pulic_pass()
    decoded = jwt.decode(jwt_encoded, pulic_rsa, algorithms=[algorithm] )
    return decoded


def read_rsa_pass() -> bytes:
    private_key = open('./id_rsa_pass', 'rb').read()
    return private_key


def read_pulic_pass() -> bytes:
    public_key = open('./id_rsa_pass.pub', 'rb').read()
    return public_key




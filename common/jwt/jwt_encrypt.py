#!/usr/bin/python
# -*- encoding: utf-8 -*-
import jwt, logging
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger('django')
RS256 = 'RS256'

def encrypt_jwt_modules(data) -> str:
    logger.debug('Criando Token JWT')
    private_rsa = read_rsa_modules()

    private_key = serialization.load_ssh_private_key(
    private_rsa, password=b''
    )
    
    encoded = jwt.encode(payload=data, key=private_key, algorithm=RS256)
    return encoded


def decrypt_jwt_modules(jwt_encoded) -> dict:
    pulic_rsa = read_pulic_modules()
    decoded = jwt.decode(jwt_encoded, pulic_rsa, algorithms=[RS256] )
    return decoded


def read_rsa_modules() -> bytes:
    private_key = open('./id_rsa_modules', 'rb').read()
    return private_key


def read_pulic_modules() -> bytes:
    public_key = open('./id_rsa_modules.pub', 'rb').read()
    return public_key


# Exemple...:

# data = {'cnpj':'02353336035'}
# jwt = encrypt_jwt_modules(data)


# data = 'eyJhbGciO...'
# te = decrypt_jwt_modules(data)
# print(te)
#!/usr/bin/python
# -*- encoding: utf-8 -*-

import bcrypt, logging

logger = logging.getLogger('django')

def encrypt_data(passwd):
	"""
		Criptografa a senha de entrada com o aes_key e iv da senha do banco
	"""
	try:
		logger.debug('Criptografando senha')
		salt = bcrypt.gensalt()
		hashed = bcrypt.hashpw(passwd.encode('utf-8'), salt)
		
		return hashed.decode('utf-8')
	except:
		logger.error('Erro ao criptografar senha')
		raise Exception('Erro ao criptografar senha')



def veryfy_pass(password, password_db) -> bool:
    """
    Verifica se as senhas são iguais criptogravadas
    """
    is_equal = bcrypt.hashpw(password.encode('utf-8'), password_db.encode('utf-8')) == password_db.encode('utf-8')

    return is_equal

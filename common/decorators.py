#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import jwt
import os

from functools import wraps
from rest_framework import status
from common.jwt.jwt_encrypt import decrypt_jwt_pass
from django.http import JsonResponse



logger = logging.getLogger('django')


def jwt_verifier(function):
    """
    Decorador para verificar Tokens JSON Web (JWT) em views do Django.

    Este decorador extrai o JWT do cabeçalho 'Authorization' na solicitação HTTP,
    decodifica e verifica o token e anexa a carga útil decodificada ao objeto de solicitação
    para processamento adicional na view decorada.

    Args:
        funcao (callable): A função de visualização a ser decorada.

    Returns:
        callable: A função de visualização decorada.

    Raises:
        JsonResponse: Retorna uma resposta JSON com uma mensagem de erro se a verificação do token falhar.

    """
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        AUTHORIZATION = request.headers.get('Authorization')

        if not AUTHORIZATION:
            message = 'Sem Token. Bad Request'
            logger.error({'results': message})
            return JsonResponse({
                'results': message
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            jwt_token = AUTHORIZATION.split()
            jwt_token_decoded = decrypt_jwt_pass(jwt_token[1])

            return function(request, jwt_token_decoded, *args, **kwargs)

        except jwt.ExpiredSignatureError as error:
            message = 'Token expirado!'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': message
            }, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidSignatureError as error:
            message = 'Token invalido!'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': 'Token invalido'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except KeyError as error:
            message = 'Token invalido!'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': 'Token invalido'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error:
            message = 'Token inesperado.'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': message
            }, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper
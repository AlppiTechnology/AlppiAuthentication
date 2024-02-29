#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import jwt


from functools import wraps
from rest_framework import status
from alppi.jwt.jwt_encrypt import decrypt_jwt_pass
from django.http import JsonResponse
from django.contrib.auth.backends import ModelBackend

from common.systemModules.system_modules import SystemModules



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
            request.jwt_token = jwt_token_decoded

            return function(request=request, *args, **kwargs)

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

def load_system_modules(function):

    @wraps(function)
    def wrapper(request, *args, **kwargs):
        try:
            SM = SystemModules()
            SM.get_modules()
            system_modules = SM.decoded_system_modules()

            request.system_modules = system_modules

            return function(request=request, *args, **kwargs)
        except Exception as error:
            message = 'Problemas ao carregar informações dos modulos disponiveis do sistema.'
            logger.error({'results': message})
            logger.error(error)
            return JsonResponse({
                'results': message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return function(request=request, *args, **kwargs)
    return wrapper

def permission_model_required(model=None):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
        
            request.model_perm = model.lower()

            return function(request=request, *args, **kwargs)
        return wrapper
    return decorator
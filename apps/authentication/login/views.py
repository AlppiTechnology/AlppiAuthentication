#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import pytz
import os

from datetime import datetime, timedelta
from django.http import JsonResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from apps.authentication.query.query_user import user_infos, user_update_last_access
from common.criptografy.hash_password import veryfy_pass
from common.criptografy.jwt_encrypt import create_jwt_pass

JWT_TOKEN_VALIDATE = os.getenv('JWT_TOKEN_VALIDATE', '5')

logger = logging.getLogger('django')
brasil_tz = pytz.timezone('America/Sao_Paulo')


class LoginView(APIView):

    def post(self, request, format=None):

        try:
            data = request.data

            user_credentials, has_error = user_infos(data)

            if has_error:
                return has_error

            if user_credentials.get('status') == False:
                message = 'Usuario Bloqueado!'
                logger.debug({'results': message})
                return JsonResponse(data={'results': message},
                                    status=status.HTTP_401_UNAUTHORIZED)

            if veryfy_pass(data.get('password'), user_credentials.get('password')):
                logger.debug('Usuario autorizado')

                _, has_error = user_update_last_access(
                    user_credentials.get('pk_user'))
                if has_error:
                    return has_error

                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip_address = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip_address = request.META.get('REMOTE_ADDR')

                token_information = {
                    'pk_user': user_credentials.get('pk_user'),
                    'registration': data.get('registration'),
                    'full_name': user_credentials.get('full_name'),
                    'status': user_credentials.get('status'),
                    'campus_code': user_credentials.get('campus_code'),
                    'pk_campus': user_credentials.get('pk_campus'),
                    'ip_adress': ip_address,
                    'exp': datetime.now() + timedelta(hours=int(JWT_TOKEN_VALIDATE))
                }

                user_jwt = create_jwt_pass(token_information)
                message = 'Gurpo de acesso autorizado!'
                logger.debug({'results': message})
                return JsonResponse(
                    {'user_access': user_jwt, }, status=status.HTTP_200_OK)

        except Exception as error:
            message = 'Problemas do servidor ao autenticar usuario.'
            logger.debug({'results': message})
            logger.error(message)
            logger.error(error)
            return JsonResponse(data={'results': message},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

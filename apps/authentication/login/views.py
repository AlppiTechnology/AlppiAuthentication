#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import pytz
import os


from datetime import datetime, timedelta
from django.http import JsonResponse, JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView

from apps.authentication.query.query_user import user_infos, user_update_last_login
from apps.authentication.modules.views import SystemModules
from common.criptografy.jwt_encrypt import create_jwt_pass

JWT_TOKEN_VALIDATE = os.getenv('JWT_TOKEN_VALIDATE', '5')

logger = logging.getLogger('django')
brasil_tz = pytz.timezone('America/Sao_Paulo')

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.login.validations import  validate_registration, validate_password
from django.contrib.auth import login, logout
from apps.authentication.login.serializer import  UserLoginSerializer, UserSerializer
from rest_framework import permissions, status


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    ##
    def post(self, request):
        data = request.data
        assert validate_registration(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

# class LoginView(APIView):

#     def post(self, request, format=None):

#         try:
#             data = request.data

#             user = authenticate(username=data.registration, password=data.password)

#             # user_credentials, has_error = user_infos(data)

#             # if has_error:
#             #     return has_error

#             # if user_credentials.get('status') == False:
#             #     message = 'Usuario Bloqueado!'
#             #     logger.debug({'results': message})
#             #     return JsonResponse(data={'results': message},
#             #                         status=status.HTTP_401_UNAUTHORIZED)
            
#             # if check_password(data.get('password'), user_credentials.get('password')):
#             #     logger.debug('Usuario autorizado')

#             #     _, has_error = user_update_last_login(
#             #         user_credentials.get('pk_user'))
#             #     if has_error:
#             #         return has_error

#             #     if 'HTTP_X_FORWARDED_FOR' in request.META:
#             #         ip_address = request.META['HTTP_X_FORWARDED_FOR']
#             #     else:
#             #         ip_address = request.META.get('REMOTE_ADDR')

#             #     token_information = {
#             #         'pk_user': user_credentials.get('pk_user'),
#             #         'registration': data.get('registration'),
#             #         'username': user_credentials.get('username'),
#             #         'status': user_credentials.get('status'),
#             #         'campus_code': user_credentials.get('campus_code'),
#             #         'pk_campus': user_credentials.get('pk_campus'),
#             #         'ip_adress': ip_address,
#             #         'exp': datetime.now() + timedelta(hours=int(JWT_TOKEN_VALIDATE))
#             #     }

#             #     user_jwt = create_jwt_pass(token_information)
#             #     message = 'Usuario autorizado!'
#             #     logger.debug({'results': message})


#             #     # Capturando Modulos de acesso da Empresa
#             #     system_modules = SystemModules().get_modules()

#                 # return JsonResponse(
#                 #     {'user_access': user_jwt, 
#                 #      'system_modules': system_modules}, status=status.HTTP_200_OK)

#             message = 'Credenciais incorretas!'
#             logger.debug({'data':message})
#             return JsonResponse(data={'data':message}, 
#                                 status=status.HTTP_401_UNAUTHORIZED)
        
#         except Exception as error:
#             message = 'Problemas do servidor ao autenticar usuario.'
#             logger.debug({'results': message})
#             logger.error(message)
#             logger.error(error)
#             return JsonResponse(data={'results': message},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

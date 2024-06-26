#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import os
import requests
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.authentication.query.query_campus import get_campus_cnpj
from alppi.jwt.jwt_encrypt import encrypt_jwt_modules

from src.systemModules.systema_modules import SystemModules

ALPPI_INTRANET = os.getenv('ALPPI_INTRANET')


logger = logging.getLogger('django')


class UpdateSystemModules(APIView):

    def get(self, request, format=None) -> Response:
        cnpj, has_error = get_campus_cnpj()
        if has_error:
            return has_error

        jwt_token: str = encrypt_jwt_modules(cnpj)

        headers: dict = {'Authorization': 'Bearer '+jwt_token}

        response = requests.get(ALPPI_INTRANET, headers=headers)

        if response.status_code == 200:
            # Exibindo o conteúdo da resposta
            jwt_modules = json.loads(response.text)

            SM = SystemModules()
            SM.set_modules(jwt_modules.get('results'))

            message = f'Modulos atualizados com sucesso.'
            return Response({'results': message}, status=status.HTTP_200_OK)
        else:
            message = f'Erro na requisição. {response.text.results}'
            return Response({'results': message}, status=status.HTTP_400_BAD_REQUEST)

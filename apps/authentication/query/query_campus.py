#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import connection
from rest_framework import status
from django.http import JsonResponse
import logging
import pytz

from datetime import datetime

logger = logging.getLogger('django')

def get_campus_cnpj() -> tuple:
    logger.info('Capturando CNPJ do campus.')
    query = 'SELECT cnpj FROM tb_campus'

    try:
        logger.info('Criando cursor no banco de dados')
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            logger.info('Executando query get_campus_cnpj')

        return ({'cnpj':row[0]}, None)

    except Exception as error:
        message = 'Problemas do servidor ao atualizar acesso do usuario.'
        logger.info({'results': message})
        logger.error(error)
        return (None, JsonResponse(data={'results': message},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR))

    finally:
        cursor.close()
        logger.info('Cursor do banco fechado')

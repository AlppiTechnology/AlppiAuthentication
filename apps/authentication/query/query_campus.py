#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging

from django.db import connection
from alppi.responses import ResponseHelper

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
        logger.error({'results': message, 'error:': str(error)})
        return (None, ResponseHelper.HTTP_500({'results': message, 'error:': str(error)}))

    finally:
        cursor.close()
        logger.info('Cursor do banco fechado')

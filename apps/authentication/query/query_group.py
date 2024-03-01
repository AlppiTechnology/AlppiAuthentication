#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import connection
from rest_framework import status
from django.http import JsonResponse
import logging
import pytz

from datetime import datetime

from alppi.responses import ResponseHelper

logger = logging.getLogger('django')


def get_user_group_info(pk_user) -> dict:
    logger.info('Capturando informações dos grupos disponiveis do usuario')
    query = 'SELECT ag.name from tb_user_groups AS ug '\
            'JOIN auth_group AS ag on ug.group_id = ag.id '\
            'WHERE ug.user_id = %s'
    vars_query = (pk_user,)
    print(query % vars_query)

    try:
        logger.info('Criando cursor no banco de dados')
        with connection.cursor() as cursor:
            cursor.execute(query, vars_query)
            row = cursor.fetchall()
            logger.info('Executando query get_user_group_info')

        if row:
            group_list = [group[0] for group in row]
            return (group_list, None)
        
        message = 'Este usuario não contem grupos!'
        logger.error({'results': message})
        return (None, ResponseHelper.HTTP_400({'results': message}))


    except Exception as error:
        message = 'Problemas do servidor buscar grupos do usuario.'
        logger.error({'results': message, 'error:': str(error)})
        return (None, ResponseHelper.HTTP_500({'results': message, 'error:': str(error)}))

    finally:
        cursor.close()
        logger.info('Cursor do banco fechado')

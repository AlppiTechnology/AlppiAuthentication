#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import connection
from rest_framework import status
from django.http import JsonResponse
import logging
import pytz

from datetime import datetime

logger = logging.getLogger('django')


def user_infos(data) -> tuple:

    query = 'SELECT u.pk_user, u.full_name, u.password, u.status, '\
        'cp.campus_code, cp.pk_campus '\
        'FROM tb_user as u '\
        'LEFT JOIN tb_campus as cp on cp.pk_campus=u.fk_campus '\
        'WHERE u.registration = %s '

    vars_query = (str(data.get('registration')),)
    print(query % vars_query)
    try:
        logger.info('Criando cursor no banco de dados')
        with connection.cursor() as cursor:
            cursor.execute(query, vars_query)
            row = cursor.fetchone()
            logger.info('Executando query user_infos')

        if row:
            return_query = {
                'pk_user': row[0],
                'full_name': row[1],
                'password': row[2],
                'status': row[3],
                'campus_code': row[4],
                'pk_campus': row[5]
            }
            return (return_query, None)

        message = 'Este usuario não existe!'
        logger.error({'results': message})
        return (None, JsonResponse({
            'results': message,
        }, status=status.HTTP_400_BAD_REQUEST))

    except Exception as error:
        message = 'Problemas do servidor ao autenticar usuario.'
        logger.info({'results': message})
        logger.error(error)
        return None, JsonResponse(data={'results': message},
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        cursor.close()
        logger.info('Cursor do banco fechado')


def user_update_last_access(id) -> tuple:
    logger.info('Atualizando ultima acesso do usuario.')
    query = 'UPDATE tb_user SET last_access = %s '\
        'WHERE  pk_user = %s '
    vars_query = (datetime.now(), str(id))

    try:
        logger.info('Criando cursor no banco de dados')
        with connection.cursor() as cursor:
            cursor.execute(query, vars_query)
            logger.info('E xecutando query user_update_last_access')

        return (True, None)

    except Exception as error:
        message = 'Problemas do servidor ao atualizar acesso do usuario.'
        logger.info({'results': message})
        logger.error(error)
        return (None, JsonResponse(data={'results': message},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR))

    finally:
        cursor.close()
        logger.info('Cursor do banco fechado')

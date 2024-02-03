import logging
import bcrypt

from django.http import JsonResponse

from rest_framework import status

logger = logging.getLogger('django')


def veryfy_pass(password, password_db) -> bool:
    """
    """
    try:
        is_equal = bcrypt.hashpw(password.encode('utf-8'), password_db.encode('utf-8')) == password_db.encode('utf-8')

        return is_equal
    except Exception as error:
        message = 'Problemas ao verificarr senha.'
        logger.debug({'results':message, 'resp_code':'MS1X01101'})
        logger.error(error)
        return JsonResponse(data={'results':message, 'resp_code':'MS1X01101'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

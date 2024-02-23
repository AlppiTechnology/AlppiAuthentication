import jwt, logging
from rest_framework import status
from django.http import JsonResponse

from common.criptografy.jwt_encrypt import decrypt_jwt_group


logger = logging.getLogger('django')
algorithm = 'RS256'


def jwt_verifier_group(request):
        AUTHORIZATION = request.headers.get('Authorization')
        if not AUTHORIZATION:
            message = 'Sem Token.'
            logger.error({'results':message, 'resp_code':'MS2X01201'})
            return (JsonResponse({
                'results': message,
                'resp_code':'MS2X01201'
            }, status=status.HTTP_401_UNAUTHORIZED), False)
        
        try:
            jwt_token = AUTHORIZATION.split()
            jwt_decoded = decrypt_jwt_group(jwt_token[1])
            return (jwt_decoded, True)
        
        except jwt.ExpiredSignatureError:

            message = 'Token expirado!'
            logger.error({'results':message, 'resp_code':'MS2X01202'})
            return (JsonResponse({
                'results': message,
                'resp_code':'MS2X01202'
            }, status=status.HTTP_401_UNAUTHORIZED), False)

        except jwt.InvalidSignatureError:
            message = 'Token invalido!'
            logger.error({'results':message, 'resp_code':'MS2X01203'})
            return (JsonResponse({
                'results': message,
                'resp_code':'MS2X01203'
            }, status=status.HTTP_401_UNAUTHORIZED), False)

        except KeyError as error:
            message = 'Token invalido!'
            logger.error({'results':message, 'resp_code':'MS2X01204'})
            return (JsonResponse({
                'results': message,
                'resp_code':'MS2X01204'
            }, status=status.HTTP_401_UNAUTHORIZED), False)
        
        except Exception as error:
            message = 'Token inesperado.'
            logger.error({'results':message, 'resp_code':'MS2X01205'})
            return (JsonResponse({
                'results': message,
                'resp_code':'MS2X01205'
            }, status=status.HTTP_401_UNAUTHORIZED), False)



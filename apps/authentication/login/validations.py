from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()


def validate_registration(data):
    registration = data['registration'].strip()
    if not registration:
        raise ValidationError('Informe o numero de matricula para o login.')
    return True


def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('Informe a senha para o login.')
    return True
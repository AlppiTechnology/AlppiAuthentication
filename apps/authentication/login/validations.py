from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()


def validate_registration(data) -> bool:
    registration = data['registration'].strip()
    if not registration:
        raise ValidationError('Informe o numero de matricula para o login.')
    return True


def validate_password(data) -> bool:
    password = data['password'].strip()
    if not password:
        raise ValidationError('Informe a senha para o login.')
    return True


def validate_level_group(user_group) -> str:
    group_list = ['superuser','administrador','coordenador',
                  'avaliador','professor','aluno']

    for group in group_list:
        if group in user_group:
            return group
        
    return next((group for group in group_list if group in user_group), None)

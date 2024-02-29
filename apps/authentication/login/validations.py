from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()


def validate_registration(data) -> bool:
    """
    Validação para garantir que o número de matrícula seja fornecido.

    Esta função verifica se o número de matrícula foi fornecido nos dados recebidos.
    Se não, levanta uma exceção de validação.

    Parâmetros:
    - data (dict): Dados contendo a chave 'registration' que representa o número de matrícula.

    Retorna:
    bool: True se o número de matrícula for fornecido corretamente.
    """
    registration = data['registration'].strip()
    if not registration:
        raise ValidationError('Informe o numero de matricula para o login.')
    return True


def validate_password(data) -> bool:
    """
    Validação para garantir que a senha seja fornecida.

    Esta função verifica se a senha foi fornecida nos dados recebidos.
    Se não, levanta uma exceção de validação.

    Parâmetros:
    - data (dict): Dados contendo a chave 'password' que representa a senha.

    Retorna:
    bool: True se a senha for fornecida corretamente.
    """
    password = data['password'].strip()
    if not password:
        raise ValidationError('Informe a senha para o login.')
    return True


def validate_level_group(user_group) -> str:
    """
    Validação para determinar o nível de acesso do grupo de usuário.

    Esta função verifica o grupo de usuário fornecido e determina o nível de acesso correspondente.
    Retorna o primeiro nível de acesso encontrado no grupo ou None se nenhum for encontrado.

    Parâmetros:
    - user_group (str): Grupo de usuário que pode conter informações sobre o nível de acesso.

    Retorna:
    str or None: O nível de acesso encontrado ou None se nenhum for encontrado.
    """
    group_list = ['superuser','administrador','coordenador',
                  'avaliador','professor','aluno']


    return next((group for group in group_list if group in user_group), None)

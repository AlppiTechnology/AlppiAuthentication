from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    registration = data['registration'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    ##
    if not registration or UserModel.objects.filter(registration=registration).exists():
        raise ValidationError('choose another registration')
    ##
    if not password or len(password) < 8:
        raise ValidationError('choose another password, min 8 characters')
    ##
    if not username:
        raise ValidationError('choose another username')
    return data


def validate_registration(data):
    registration = data['registration'].strip()
    if not registration:
        raise ValidationError('an registration is needed')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True
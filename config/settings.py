"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import date
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = [
    host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') 
    if host.strip()]


# Application definition
CUSTOM_APPS = [
    'rest_framework',
    'api.v1',
    'apps.authentication'
]

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'rest_framework',
    'api.v1',
    'apps.authentication'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.getenv('DB_ENGINE_1'),
        'NAME': os.getenv('DB_NAME_1'),
        'USER': os.getenv('DB_USER_1'),
        'PASSWORD': os.getenv('DB_PASSWORD_1'),
        'HOST': os.getenv('DB_HOST_1'),
        'PORT': os.getenv('DB_PORT_1')
    },
    "database_2": {
        "ENGINE": os.getenv('DB_ENGINE_2'),
        'NAME': os.getenv('DB_NAME_2'),
        'USER': os.getenv('DB_USER_2'),
        'PASSWORD': os.getenv('DB_PASSWORD_2'),
        'HOST': os.getenv('DB_HOST_2'),
        'PORT': os.getenv('DB_PORT_2')
    }
}

# Configuração do logger
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

LOGGING_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO") # Defina o nível de registro desejado (DEBUG, INFO, etc.)
ROOT_LOGGIN_LEVEL = 'INFO'
LOG_FILE_PATH = os.path.join(LOGGING_DIR, f"{date.today()}.log")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {module} {process:d} {thread:d} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'file': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'verbose',
        }
    },
    'root': {
        'handlers': ['console','file'],
        'level': ROOT_LOGGIN_LEVEL,  # Defina o nível de log conforme necessário
    },
     'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
    },
}

# CONFIGURAÇÃO DE PAGINATOR PARA O DRF
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S",
    'DATE_FORMAT':'%Y-%m-%d',
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

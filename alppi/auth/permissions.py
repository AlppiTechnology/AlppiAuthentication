#!/usr/bin/python
# -*- encoding: utf-8 -*-
import logging
import os

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from apps.register.models import User


logger = logging.getLogger('django')

ALPPIDEVEL = os.getenv('ALPPIDEVEL')

class IsAuthenticatedAlppi(BasePermission):

    def has_permission(self, request, view):
        self.get_user(request)
        model = request.model_perm
        # Mapear métodos para permissões específicas (ajuste conforme necessário)
        method_permissions = {
            'GET': f'view_{model}',
            'POST': f'add_{model}',
            'PUT': f'change_{model}',
            'PATCH': f'change_{model}',
            'DELETE': f'delete_{model}'
        }

        # Obter a permissão necessária com base no método da requisição
        required_permission = method_permissions.get(request.method, None)
        
        # permissão de deleção somente para usuarios ALPPI
        if required_permission.startswith('delete_') and not request.user.is_superuser:
            return False

        if request.user.has_perm(required_permission):
            return True

        if not required_permission:
            # Método não suportado, negar acesso
            return False

        # Verificar as permissões na tabela auth_user_user_permissions
        user_permissions = request.user.user_permissions.all()
        if any(permission.codename == required_permission for permission in user_permissions):
            return True

        # Verificar as permissões na tabela auth_user_groups
        user_groups = request.user.groups.all()
        for group in user_groups:
            group_permissions = group.permissions.all()
            if any(permission.codename == required_permission for permission in group_permissions):
                return True

        # Se nenhuma permissão foi encontrada, negar acesso
        # return False
        raise PermissionDenied("Este usuario não tem permissão para acessar esta rota.")


    def get_user(self, request):
        pk_user = request.jwt_token.get('pk_user')
        user = User.objects.get(pk=pk_user)
        request.user  = user
        
        return True if user else False


class IsViewAllowed(BasePermission):

    def has_object_permission(self,request, view, obj):
        return self.get_user(request)

    def get_user(self, request):
        try:
            registration = request.jwt_token.get('registration')
            user = User.objects.get(registration=registration)
            request.user  = user

            if not request.user.is_active:
                logger.error({'results': 'Usuario inativo.'})
                return False
            
            return True if user else False
        except User.DoesNotExist:
            message = 'Não foi possivel encontrar este User.'
            logger.error({'results': message})
            return False

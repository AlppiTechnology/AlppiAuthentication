#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):

    first_name = False
    last_name = False
    pk_user = models.AutoField(primary_key=True, unique=True)
    registration = models.CharField(unique=True, null=False, max_length=6)
    password = models.TextField(null=False)

    USERNAME_FIELD = 'registration'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = "tb_user"
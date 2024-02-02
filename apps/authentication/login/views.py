#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.http import JsonResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView



from datetime import datetime, timedelta
import logging
import pytz
import os

logger = logging.getLogger('django')
brasil_tz = pytz.timezone('America/Sao_Paulo')


class LoginView(APIView):

    def post(self, request, format=None):
        data = request.data
        pass
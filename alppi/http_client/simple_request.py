#!/usr/bin/python
# -*- encoding: utf-8 -*-
import requests, logging, json

logger = logging.getLogger('django')


class HttpClient:
    def __init__(self, base_url, default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {}

    def _make_request(self, method, endpoint, params=None, data=None, headers=None, cookies=None, auth=None):
        url = f"{self.base_url}/{endpoint}"
        final_headers = {**self.default_headers, **(headers or {})}
        
        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=data,
                headers=final_headers,
                cookies=cookies,
                auth=auth
            )
            
            response.raise_for_status()  # Lança exceção se a resposta indicar um erro HTTP

            return response.json() if response.headers.get('content-type') == 'application/json' else response.text
        except requests.exceptions.RequestException as e:
            # Trata exceções relacionadas a problemas de rede ou respostas HTTP de erro
            raise HttpException(f"Erro na requisição HTTP: {str(e)}")

    def get(self, endpoint, params=None, headers=None, cookies=None, auth=None):
        return self._make_request("GET", endpoint, params=params, headers=headers, cookies=cookies, auth=auth)

    def post(self, endpoint, data=None, headers=None, cookies=None, auth=None):
        return self._make_request("POST", endpoint, data=data, headers=headers, cookies=cookies, auth=auth)

    def put(self, endpoint, data=None, headers=None, cookies=None, auth=None):
        return self._make_request("PUT", endpoint, data=data, headers=headers, cookies=cookies, auth=auth)

    def delete(self, endpoint, headers=None, cookies=None, auth=None):
        return self._make_request("DELETE", endpoint, headers=headers, cookies=cookies, auth=auth)

class HttpException(Exception):
    pass

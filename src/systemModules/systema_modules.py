#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import logging

class SystemModules:


    def get_modules(self) -> str:
        if os.path.exists('./alppi.key'):

            alppi_key: str = './alppi.key'
            with open(alppi_key, 'r') as arquivo:
                # Carregar o conteúdo do arquivo JSON
                modules_jwt = arquivo.read()

            return modules_jwt
        
        else:
            return None
        
    def set_modules(self, jwt_modules: str) -> str:
        try:
            if os.path.exists('./alppi.key'):

                alppi_key: str = './alppi.key'
                with open(alppi_key, 'w') as arquivo:
                    # Carregar o conteúdo do arquivo JSON
                    arquivo.write(jwt_modules)
                    return 'Modulos Atualizados com sucesso'

        except Exception as e:
            return f'Erro ao atualizar modulos: {e}'
            
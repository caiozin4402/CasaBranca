# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.errorResponse import ErrorResponse

class ChaleMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Chale.

    Objetivos:
    - Garantir que os dados obrigatórios estejam presentes antes de chamar
      os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição (JSON) para operações de Chale.

        Verifica apenas a existência:
        - O objeto 'Chale' existe
        - O campo obrigatório 'nomeChale' está presente
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ChaleMiddleware.validate_body()")
            body = request.get_json()

            if not body or 'Chale' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'Chale' é obrigatório!"}
                )

            Chale = body['Chale']
            if 'nome' not in Chale:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nome' é obrigatório!"}
                )

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'idChale'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ChaleMiddleware.validate_id_param()")
            if 'idChale' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'idChale' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function
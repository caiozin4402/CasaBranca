# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.errorResponse import ErrorResponse

class InquilinoMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Inquilino.

    Objetivos:
    - Garantir que os dados obrigatórios estejam presentes antes de chamar
      os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição (JSON) para operações de Inquilino.

        Verifica apenas a existência:
        - O objeto 'Inquilino' existe
        - O campo obrigatório 'nomeInquilino' está presente
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 InquilinoMiddleware.validate_body()")
            body = request.get_json()

            if not body or 'Inquilino' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'Inquilino' é obrigatório!"}
                )

            Inquilino = body['Inquilino']
            if 'nomeInquilino' not in Inquilino:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nomeInquilino' é obrigatório!"}
                )

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'idInquilino'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 InquilinoMiddleware.validate_id_param()")
            if 'idInquilino' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'idInquilino' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function
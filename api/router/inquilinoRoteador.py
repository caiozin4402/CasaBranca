# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.inquilinoMiddleware import InquilinoMiddleware
from api.controle.inquilinoControl import InquilinoControl

class InquilinoRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Inquilino no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Inquilino.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, Inquilino_middleware: InquilinoMiddleware, Inquilino_control: InquilinoControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param Inquilino_middleware: Middleware com validações específicas para Inquilino (ex.: validação de corpo, id).
        :param Inquilino_control: Controlador que implementa a lógica de negócio (store, index, update, delete, show).

        Observações:
        - Blueprint é criado para permitir o registro isolado de rotas.
        - Injeção de dependência garante desacoplamento: o roteador não precisa criar middlewares ou controlador.
        """
        print("⬆️  InquilinoRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__Inquilino_middleware = Inquilino_middleware
        self.__Inquilino_control = Inquilino_control

        # Blueprint é a coleção de rotas da entidade Inquilino
        self.__blueprint = Blueprint('Inquilino', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Inquilino.

        Rotas implementadas:
        - POST /        -> Cria um novo Inquilino
        - GET /         -> Lista todos os Inquilinos
        - GET /<id>     -> Retorna um Inquilino por ID
        - PUT /<id>     -> Atualiza um Inquilino por ID
        - DELETE /<id>  -> Remove um Inquilino por ID

        Observações:
        - Cada rota aplica autenticação JWT.
        - Middlewares de validação são aplicados diretamente.
        - Para rotas que precisam do idInquilino, o parâmetro vem da URI.
        """

        # POST / -> cria um Inquilino
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__Inquilino_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo Inquilino.
            O corpo da requisição deve conter os dados do Inquilino validados pelo middleware.
            """
            return self.__Inquilino_control.store()

        # GET / -> lista todos os Inquilinos
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT

        def index():
            """
            Rota responsável por listar todos os Inquilinos cadastrados no sistema.
            """
            return self.__Inquilino_control.index()

        # GET /<idInquilino> -> retorna um Inquilino específico
        @self.__blueprint.route('/<int:idInquilino>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__Inquilino_middleware.validate_id_param  # valida se o ID é válido
        def show(idInquilino):
            """
            Rota que retorna um Inquilino específico pelo seu ID.

            :param idInquilino: int - ID do Inquilino vindo da URI.
            """
            return self.__Inquilino_control.show()

        # PUT /<idInquilino> -> atualiza um Inquilino
        @self.__blueprint.route('/<int:idInquilino>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__Inquilino_middleware.validate_id_param
        @self.__Inquilino_middleware.validate_body

        def update(idInquilino):
            """
            Rota que atualiza um Inquilino existente.

            Observações:
            - idInquilino vem da URI (request.view_args['idInquilino']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__Inquilino_control.update()

        # DELETE /<idInquilino> -> remove um Inquilino
        @self.__blueprint.route('/<int:idInquilino>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__Inquilino_middleware.validate_id_param
        
        def destroy(idInquilino):
            """
            Rota que remove um Inquilino pelo seu ID.

            :param idInquilino: int - ID do Inquilino a ser removido.
            """
            return self.__Inquilino_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint
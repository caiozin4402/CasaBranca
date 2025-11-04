# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.chaleMiddleware import ChaleMiddleware
from api.controle.chaleControl import ChaleControl

class ChaleRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Chale no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Chale.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, Chale_middleware: ChaleMiddleware, Chale_control: ChaleControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param Chale_middleware: Middleware com validações específicas para Chale (ex.: validação de corpo, id).
        :param Chale_control: Controlador que implementa a lógica de negócio (store, index, update, delete, show).

        Observações:
        - Blueprint é criado para permitir o registro isolado de rotas.
        - Injeção de dependência garante desacoplamento: o roteador não precisa criar middlewares ou controlador.
        """
        print("⬆️  ChaleRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__Chale_middleware = Chale_middleware
        self.__Chale_control = Chale_control

        # Blueprint é a coleção de rotas da entidade Chale
        self.__blueprint = Blueprint('Chale', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Chale.

        Rotas implementadas:
        - POST /        -> Cria um novo Chale
        - GET /         -> Lista todos os Chales
        - GET /<id>     -> Retorna um Chale por ID
        - PUT /<id>     -> Atualiza um Chale por ID
        - DELETE /<id>  -> Remove um Chale por ID

        Observações:
        - Cada rota aplica autenticação JWT.
        - Middlewares de validação são aplicados diretamente.
        - Para rotas que precisam do idChale, o parâmetro vem da URI.
        """

        # POST / -> cria um Chale
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__Chale_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo Chale.
            O corpo da requisição deve conter os dados do Chale validados pelo middleware.
            """
            return self.__Chale_control.store()

        # GET / -> lista todos os Chales
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os Chales cadastrados no sistema.
            """
            return self.__Chale_control.index()

        # GET /<idChale> -> retorna um Chale específico
        @self.__blueprint.route('/<int:idChale>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__Chale_middleware.validate_id_param  # valida se o ID é válido
        def show(idChale):
            """
            Rota que retorna um Chale específico pelo seu ID.

            :param idChale: int - ID do Chale vindo da URI.
            """
            return self.__Chale_control.show()

        # PUT /<idChale> -> atualiza um Chale
        @self.__blueprint.route('/<int:idChale>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__Chale_middleware.validate_id_param
        @self.__Chale_middleware.validate_body
        def update(idChale):
            """
            Rota que atualiza um Chale existente.

            Observações:
            - idChale vem da URI (request.view_args['idChale']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__Chale_control.update()

        # DELETE /<idChale> -> remove um Chale
        @self.__blueprint.route('/<int:idChale>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__Chale_middleware.validate_id_param
        def destroy(idChale):
            """
            Rota que remove um Chale pelo seu ID.

            :param idChale: int - ID do Chale a ser removido.
            """
            return self.__Chale_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint
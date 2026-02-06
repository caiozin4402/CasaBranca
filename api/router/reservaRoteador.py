# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.reservaMiddleware import ReservaMiddleware
from api.controle.reservaControl import ReservaControl

class ReservaRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Reserva no Flask.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, Reserva_middleware: ReservaMiddleware, Reserva_control: ReservaControl):
        print("⬆️  ReservaRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__Reserva_middleware = Reserva_middleware
        self.__Reserva_control = Reserva_control

        # Blueprint é a coleção de rotas da entidade Reserva
        self.__blueprint = Blueprint('Reserva', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Reserva.
        """

        # POST / -> cria um Reserva
        @self.__blueprint.route('/', methods=['POST'])
        #@self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__Reserva_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo Reserva.
            O corpo da requisição deve conter os dados do Reserva validados pelo middleware.
            """
            return self.__Reserva_control.store()

        # GET / -> lista todos os Reservas
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os Reservas cadastrados no sistema.
            """
            return self.__Reserva_control.index()

        # GET /<idReserva> -> retorna um Reserva específico
        @self.__blueprint.route('/<int:idReserva>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__Reserva_middleware.validate_id_param  # valida se o ID é válido
        def show(idReserva):
            """
            Rota que retorna um Reserva específico pelo seu ID.

            :param idReserva: int - ID do Reserva vindo da URI.
            """
            return self.__Reserva_control.show()

        # PUT /<idReserva> -> atualiza um Reserva
        @self.__blueprint.route('/<int:idReserva>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__Reserva_middleware.validate_id_param
        @self.__Reserva_middleware.validate_body
        def update(idReserva):
            """
            Rota que atualiza um Reserva existente.

            Observações:
            - idReserva vem da URI (request.view_args['idReserva']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__Reserva_control.update()

        # DELETE /<idReserva> -> remove um Reserva
        @self.__blueprint.route('/<int:idReserva>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__Reserva_middleware.validate_id_param
        def destroy(idReserva):
            """
            Rota que remove um Reserva pelo seu ID.

            :param idReserva: int - ID do Reserva a ser removido.
            """
            return self.__Reserva_control.destroy()

        # ===================================================
        # 🆕 NOVA ROTA: RESERVA PÚBLICA (SEM AUTENTICAÇÃO)
        # ===================================================
        @self.__blueprint.route('/publica', methods=['POST'])
        def reserva_publica():
            """
            Rota PÚBLICA para reservas via site.
            Qualquer pessoa pode acessar sem token.
            """
            print("✅ ROTA /publica CHAMADA VIA POST")
            print("🌐 ROTA /publica ACESSADA (SEM JWT)")
            
            try:
                # Importar aqui para evitar import circular
                from api.controle.reservaPublicaControl import ReservaPublicaControl
                
                # Obter o serviço de reserva do controlador existente
                reserva_service = self.__Reserva_control._ReservaControl__Reserva_service
                
                # Criar controlador público
                control_publico = ReservaPublicaControl(reserva_service)
                
                # Executar
                return control_publico.store_publica()
                
            except ImportError as e:
                print(f"❌ Erro de importação: {e}")
                from flask import jsonify
                return jsonify({
                    "success": False,
                    "error": "Módulo reservaPublicaControl não encontrado"
                }), 500
            except Exception as e:
                print(f"❌ Erro na rota /publica: {e}")
                from flask import jsonify
                return jsonify({
                    "success": False,
                    "error": f"Erro interno: {str(e)}"
                }), 500

        print(f"✅ Blueprint 'Reserva' criado com rotas: /, /<idReserva>, /publica")
        return self.__blueprint

    
        
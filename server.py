from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from werkzeug.exceptions import HTTPException, NotFound

from api.database.database import DatabaseConfig
from api.utils.errorResponse import ErrorResponse
from api.utils.logger import Logger

# Middlewares
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.inquilinoMiddleware import InquilinoMiddleware
from api.Middleware.chaleMiddleware import ChaleMiddleware
from api.Middleware.reservaMiddleware import ReservaMiddleware

# Controls
from api.controle.inquilinoControl import InquilinoControl
from api.controle.chaleControl import ChaleControl
from api.controle.reservaControl import ReservaControl

# Services
from api.service.inquilinoService import InquilinoService
from api.service.chaleService import ChaleService
from api.service.reservaService import ReservaService

# DAOs
from api.dao.inquilinoDAO import InquilinoDAO
from api.dao.chaleDAO import ChaleDAO
from api.dao.reservaDAO import ReservaDAO
from api.dao.usuariosDAO import UsuarioDAO


# Routers
from api.router.inquilinoRoteador import InquilinoRoteador
from api.router.chaleRoteador import ChaleRoteador
from api.router.reservaRoteador import ReservaRoteador
from api.router.authRoteador import AuthRoteador

import traceback


class Server:
    """
    Classe principal do servidor Flask.

    Responsável por inicializar middlewares, roteadores e gerenciar a aplicação.
    """

    def __init__(self, porta: int = 8000):
        # 🔹 Porta em que o servidor irá rodar
        self.__porta = porta

        # 🔹 Instância Flask, configurando pasta de arquivos estáticos
        self.__app = Flask(__name__, static_folder="static", static_url_path="")

        # 🔹 Configuração de CORS (Cross-Origin Resource Sharing)
        #    Permite que clientes de outros domínios/portas acessem sua API
        #    Exemplo: permitir todos os domínios (somente para desenvolvimento)
        # 🔹 Configuração de CORS (Cross-Origin Resource Sharing)
#    Permite que frontend acesse a API de forma controlada
        CORS(self.__app, 
            origins=[
                "http://localhost", 
                "http://127.0.0.1:8000", 
                "http://localhost:5500", 
                "http://127.0.0.1:5500",
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ],
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=[
                "Content-Type", 
                "Authorization", 
                "X-Requested-With",
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Headers",
                "Access-Control-Allow-Methods"
            ],
            supports_credentials=True,
            expose_headers=["Content-Range", "X-Content-Range"],
            max_age=3600)

        # 🔹 Middlewares
        self.__jwt_middleware = JwtMiddleware()
        self.__inquilino_middleware = InquilinoMiddleware()
        self.__chale_middleware = ChaleMiddleware()
        self.__reserva_middleware = ReservaMiddleware()

        # 🔹 DAOs, Services e Controls serão inicializados após conexão com DB
        self.__inquilino_dao = None
        self.__chale_dao = None
        self.__reserva_dao = None
        self.__inquilino_service = None
        self.__chale_service = None
        self.__reserva_service = None
        self.__inquilino_control = None
        self.__chale_control = None
        self.__reserva_control = None
        self.__usuario_dao = None
        

        # 🔹 Conexão global com o banco
        self.__db_connection = None

    def init(self):
        """
        Inicializa a aplicação:
        - Conexão com o banco
        - Middlewares
        - Roteadores
        """
        # Middleware para parsing JSON já é nativo do Flask
        # Middleware para arquivos estáticos já configurado na criação do Flask

        # 🔹 Middleware de log antes das rotas
        self.__before_routing()

        # 🔹 Conexão global com MySQL (injeção de dependência)
        self.__db_connection = DatabaseConfig(
            pool_name="mypool",
            pool_size=10,
            host="127.0.0.1",
            user="root",
            password="85252317b",
            database="casa_branca",
            port=3306
        )

        self.__db_connection.connect()

        # 🔹 Configuração do módulo Inquilino
        self.__setup_inquilino()

        # 🔹 Configuração do módulo Chale
        self.__setup_chale()

        # 🔹 Configuração do módulo Reserva
        self.__setup_reserva()

        # 🔹 Configuração do módulo Aut
        self.__setup_auth()

        # 🔹 Middleware global de tratamento de erros
        self.__error_middleware()

    def __setup_inquilino(self):
        """Configura o módulo Inquilino (DAO, Service, Control, Router)"""
        print("⬆️  Setup Inquilino")

        # DAO recebe conexão global com o banco (injeção de dependência)
        self.__inquilino_dao = InquilinoDAO(self.__db_connection)

        # Service recebe DAO (injeção de dependência)
        self.__inquilino_service = InquilinoService(self.__inquilino_dao)

        # Controller recebe Service (injeção de dependência)
        self.__inquilino_control = InquilinoControl(self.__inquilino_service)

        # Router recebe Controller + Middlewares
        inquilino_router = InquilinoRoteador(
            self.__jwt_middleware,
            self.__inquilino_middleware,
            self.__inquilino_control
        )

        # Registra rotas da entidade Inquilino
        self.__app.register_blueprint(inquilino_router.create_routes(), url_prefix="/api/v1/inquilinos")

    def __setup_chale(self):
        """Configura o módulo Chale (DAO, Service, Control, Router)"""
        print("⬆️  Setup Chale")

        # DAO recebe conexão global com o banco (injeção de dependência)
        self.__chale_dao = ChaleDAO(self.__db_connection)

        # Service recebe DAO via injeção de dependência
        self.__chale_service = ChaleService(self.__chale_dao)

        # Controller recebe Service
        self.__chale_control = ChaleControl(self.__chale_service)

        # Router recebe Controller + Middlewares
        chale_router = ChaleRoteador(
            self.__jwt_middleware,
            self.__chale_middleware,
            self.__chale_control
        )

        # Registra rotas da entidade Chale
        self.__app.register_blueprint(chale_router.create_routes(), url_prefix="/api/v1/chales")

    def __setup_reserva(self):
        """Configura o módulo Reserva (DAO, Service, Control, Router)"""
        print("⬆️  Setup Reserva")

        # DAO
        self.__reserva_dao = ReservaDAO(self.__db_connection)

        # garante DAOs dependentes
        if self.__inquilino_dao is None:
            self.__inquilino_dao = InquilinoDAO(self.__db_connection)
        if self.__chale_dao is None:
            self.__chale_dao = ChaleDAO(self.__db_connection)

        # Service
        self.__reserva_service = ReservaService(self.__reserva_dao, self.__inquilino_dao, self.__chale_dao)

        # Controller
        self.__reserva_control = ReservaControl(self.__reserva_service)

        # Router
        reserva_router = ReservaRoteador(
            self.__jwt_middleware,
            self.__reserva_middleware,
            self.__reserva_control
        )
        self.__app.register_blueprint(reserva_router.create_routes(), url_prefix="/api/v1/reservas")

    def __setup_auth(self):
        """Configura autenticação"""
        print("⬆️  Setup Auth")
        auth_router = AuthRoteador(self.__db_connection)  # Passa conexão
        self.__app.register_blueprint(auth_router.create_routes(), url_prefix="/api/v1/auth")

    def __before_routing(self):
        """Middleware que loga separador antes de cada requisição"""
    
        # 🔥 NOVAS ROTAS PARA SERVIR OS ARQUIVOS HTML
        @self.__app.route('/Inquilinos.html')
        def serve_inquilinos():
            print("📄 Servindo Inquilinos.html")
            return send_from_directory(self.__app.static_folder, 'Inquilinos.html')
        
        @self.__app.route('/Chales.html')
        def serve_chales():
            print("📄 Servindo Chales.html")
            return send_from_directory(self.__app.static_folder, 'Chales.html')
        
        @self.__app.route('/Reservas.html')
        def serve_reservas():
            print("📄 Servindo Reservas.html")
            return send_from_directory(self.__app.static_folder, 'Reservas.html')
        
        @self.__app.route('/dashboard.html')
        def serve_dashboard():
            print("📄 Servindo dashboard.html")
            return send_from_directory(self.__app.static_folder, 'dashboard.html')

        @self.__app.before_request
        def log_separator():
            print("-" * 70)

        # rota para servir a página de login na raiz '/'
        @self.__app.route('/', methods=['GET'])
        def serve_root():
            # envia o arquivo static/login.html
            return send_from_directory(self.__app.static_folder, 'login.html')

    def __error_middleware(self):
        """Middleware global de tratamento de erros"""
        @self.__app.errorhandler(Exception)
        def handle_error(error):
           

            # 🔹 404 - Rota ou arquivo não encontrado
            if isinstance(error, NotFound):
                return error, 404

            # 🔹 Captura ErrorResponse customizado
            if isinstance(error, ErrorResponse):
                print("🟡 Server.error_middleware()")
                # Extrai stack trace como string
                stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

                Logger.log_error(error)  # Loga a exceção real

                resposta = {
                    "success": False,
                    "error": {
                        "message": str(error),
                        "code": getattr(error, "code", None),
                        "details": getattr(error, "error", None)
                    },
                    "data": {
                        "message": "Erro tratado pela aplicação",
                        "stack": stack_str
                    }
                }
                return jsonify(resposta), error._httpCode

            # 🔹 Outros erros internos (não tratados)
            stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            print("🟡 Server.error_middleware()")
            resposta = {
                "success": False,
                "error": {
                    "message": str(error),
                    "code": getattr(error, "code", None)
                },
                "data": {
                    "message": "Ocorreu um erro interno no servidor",
                    "stack": stack_str
                }
            }

            Logger.log_error(error)  # Loga a exceção real
            return jsonify(resposta), 500

    def run(self):
        """Inicia o servidor Flask na porta configurada"""
        print(f"🚀 Servidor rodando em: http://127.0.0.1:{self.__porta}")
        # ⚠️ debug=False é necessário para que o errorhandler global capture exceções
        self.__app.run(port=self.__porta, debug=False)

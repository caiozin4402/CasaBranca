import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, NotFound
from dotenv import load_dotenv  # ✅ ADICIONAR

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

# ✅ Carrega variáveis de ambiente
load_dotenv()

class Server:
    """
    Classe principal do servidor Flask.
    Responsável por inicializar middlewares, roteadores e gerenciar a aplicação.
    """

    def __init__(self, porta: int = None):
        # ✅ Porta dinâmica do ambiente ou padrão 8000
        self.__porta = porta or int(os.environ.get('PORT', 8000))

        # Instância Flask
        self.__app = Flask(__name__, static_folder="static", static_url_path="")

        # ✅ CORS configurado
        CORS(self.__app, resources={
            r"/api/*": {
                "origins": [
                    "https://caiozin4402.github.io",
                    "http://127.0.0.1:8000",
                    "http://localhost:8000"
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })

        # Middlewares
        self.__jwt_middleware = JwtMiddleware()
        self.__inquilino_middleware = InquilinoMiddleware()
        self.__chale_middleware = ChaleMiddleware()
        self.__reserva_middleware = ReservaMiddleware()

        # DAOs, Services e Controls
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
        self.__db_connection = None

    def init(self):
        """Inicializa a aplicação"""
        self.__before_routing()

        # ✅ Conexão com MySQL usando variáveis de ambiente
        self.__db_connection = DatabaseConfig(
            pool_name="mypool",
            pool_size=10,
            host=os.environ.get('DB_HOST', '127.0.0.1'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', '85252317b'),
            database=os.environ.get('DB_NAME', 'casa_branca'),
            port=int(os.environ.get('DB_PORT', 3306))
        )

        self.__db_connection.connect()

        self.__setup_inquilino()
        self.__setup_chale()
        self.__setup_reserva()
        self.__setup_auth()
        self.__error_middleware()

    def __setup_inquilino(self):
        """Configura o módulo Inquilino"""
        print("⬆️  Setup Inquilino")
        self.__inquilino_dao = InquilinoDAO(self.__db_connection)
        self.__inquilino_service = InquilinoService(self.__inquilino_dao)
        self.__inquilino_control = InquilinoControl(self.__inquilino_service)
        inquilino_router = InquilinoRoteador(
            self.__jwt_middleware,
            self.__inquilino_middleware,
            self.__inquilino_control
        )
        self.__app.register_blueprint(inquilino_router.create_routes(), url_prefix="/api/v1/inquilinos")

    def __setup_chale(self):
        """Configura o módulo Chale"""
        print("⬆️  Setup Chale")
        self.__chale_dao = ChaleDAO(self.__db_connection)
        self.__chale_service = ChaleService(self.__chale_dao)
        self.__chale_control = ChaleControl(self.__chale_service)
        chale_router = ChaleRoteador(
            self.__jwt_middleware,
            self.__chale_middleware,
            self.__chale_control
        )
        self.__app.register_blueprint(chale_router.create_routes(), url_prefix="/api/v1/chales")

    def __setup_reserva(self):
        """Configura o módulo Reserva"""
        print("⬆️  Setup Reserva")
        self.__reserva_dao = ReservaDAO(self.__db_connection)
        if self.__inquilino_dao is None:
            self.__inquilino_dao = InquilinoDAO(self.__db_connection)
        if self.__chale_dao is None:
            self.__chale_dao = ChaleDAO(self.__db_connection)
        self.__reserva_service = ReservaService(self.__reserva_dao, self.__inquilino_dao, self.__chale_dao)
        self.__reserva_control = ReservaControl(self.__reserva_service)
        reserva_router = ReservaRoteador(
            self.__jwt_middleware,
            self.__reserva_middleware,
            self.__reserva_control
        )
        self.__app.register_blueprint(reserva_router.create_routes(), url_prefix="/api/v1/reservas")

    def __setup_auth(self):
        """Configura autenticação"""
        print("⬆️  Setup Auth")
        auth_router = AuthRoteador(self.__db_connection)
        self.__app.register_blueprint(auth_router.create_routes(), url_prefix="/api/v1/auth")

    def __before_routing(self):
        """Middleware e rotas HTML"""

        # ✅ Rota raiz com health check (SOMENTE UMA!)
        @self.__app.route('/', methods=['GET'])   
        def health_check():
            return jsonify({
                "status": "online",
                "message": "Casa Branca API está rodando!",
                "endpoints": [
                    "/api/v1/auth/login",
                    "/api/v1/chales",
                    "/api/v1/inquilinos",
                    "/api/v1/reservas"
                ]
            }), 200

        # Rotas HTML
        @self.__app.route('/Inquilinos.html')
        def serve_inquilinos():
            return send_from_directory(self.__app.static_folder, 'Inquilinos.html')
        
        @self.__app.route('/Chales.html')
        def serve_chales():
            return send_from_directory(self.__app.static_folder, 'Chales.html')
        
        @self.__app.route('/Reservas.html')
        def serve_reservas():
            return send_from_directory(self.__app.static_folder, 'Reservas.html')
        
        @self.__app.route('/dashboard.html')
        def serve_dashboard():
            return send_from_directory(self.__app.static_folder, 'dashboard.html')

        @self.__app.route('/login.html')
        def serve_login():
            return send_from_directory(self.__app.static_folder, 'login.html')

        @self.__app.route('/static/<path:filename>')
        def serve_static_files(filename):
            return send_from_directory(self.__app.static_folder, filename)

        @self.__app.before_request
        def log_separator():
            print("-" * 70)

    def __error_middleware(self):
        """Middleware global de tratamento de erros"""
        @self.__app.errorhandler(Exception)
        def handle_error(error):
            if isinstance(error, NotFound):
                return error, 404

            if isinstance(error, ErrorResponse):
                stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
                Logger.log_error(error)
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

            stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
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
            Logger.log_error(error)
            return jsonify(resposta), 500

    def run(self):
        """Inicia o servidor Flask"""
        print(f"🚀 Servidor rodando em: http://0.0.0.0:{self.__porta}")
        # ✅ Configurado para produção
        self.__app.run(
            host='0.0.0.0',
            port=self.__porta,
            debug=False
        )


# ✅ FORA DA CLASSE - inicialização correta
if __name__ == '__main__':
    server = Server()
    server.init()
    server.run()
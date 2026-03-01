from server import Server

"""
Arquivo principal de inicialização do servidor Flask.

Responsabilidades:
- Cria a instância do servidor
- Inicializa todas as dependências (banco, middlewares, rotas)
- Inicia o servidor na porta especificada
"""

# ✅ Cria e inicializa o servidor
server = Server()
server.init()

# ✅ Exporta o app Flask para o Gunicorn
app = server._Server__app

def main():
    try:
        # Inicia servidor Flask
        server.run()
        print("✅ Servidor iniciado com sucesso")
    except Exception as error:
        print("❌ Erro ao iniciar o servidor:", error)

# ✅ Só executa main() quando rodado diretamente (não pelo Gunicorn)
if __name__ == '__main__':
    main()
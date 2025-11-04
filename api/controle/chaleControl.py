from flask import request, jsonify
from api.service.chaleService import ChaleService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Chale.

Esta classe implementa métodos CRUD e utiliza injeção de dependência
para receber a instância de ChaleService, desacoplando a lógica de negócio
da camada de controle.
"""
class ChaleControl:
    def __init__(self, Chale_service:ChaleService):
        """
        Construtor da classe ChaleControl
        :param Chale_service: Instância do ChaleService (injeção de dependência)
        """
        print("⬆️  ChaleControl.constructor()")
        self.__Chale_service = Chale_service

    def store(self):
        """Cria um novo Chale"""
        print("🔵 ChaleControle.store()")
       
        Chale_body_request = request.json.get("Chale")  #Pega os dados do Chale no corpo da requisição
        novo_id = self.__Chale_service.createChale(Chale_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "Chales": [
                    {
                        "idChale": novo_id,
                        "nomeChale": Chale_body_request.get("nome"),
                        "capacidade": Chale_body_request.get("capacidade"),
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        """Lista todos os Chales cadastrados"""
        print("🔵 ChaleControle.index()")
       
        array_Chales = self.__Chale_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"Chales": array_Chales}
        }), 200
        

    def show(self):
          # Pega o idChale diretamente da URI
        idChale = request.view_args.get("idChale")

        Chale = self.__Chale_service.findById(idChale)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"Chales": Chale}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        """Atualiza os dados de um Chale existente"""
        print("🔵 ChaleControle.update()")
       
        # Pega o idChale diretamente da URI
        idChale = request.view_args.get("idChale")

        # Pega os dados do Chale no corpo da requisição
        json_Chale = request.json.get("Chale")
        print(json_Chale)

        resposta = self.__Chale_service.updateChale(idChale, json_Chale)
        return jsonify({
            "success": True,
            "message": "Chale atualizado com sucesso",
            "data": {
                "Chale": {
                    "idChale": int(idChale),
                    "nomeChale": json_Chale.get("nome"),
                    "capacidade": json_Chale.get("capacidade")
                }
            }
        }), 200
   

    def destroy(self):
        """Remove um Chale pelo ID"""
        print("🔵 ChaleControle.destroy()")
        # Pega o idChale diretamente da URI
        idChale = request.view_args.get("idChale")
        
        excluiu = self.__Chale_service.deleteChale(idChale)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Chale com id {idChale}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 200
        
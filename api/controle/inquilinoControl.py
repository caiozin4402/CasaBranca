from flask import request, jsonify
from api.service.inquilinoService import InquilinoService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Inquilino.

Esta classe implementa métodos CRUD e utiliza injeção de dependência
para receber a instância de InquilinoService, desacoplando a lógica de negócio
da camada de controle.
"""
class InquilinoControl:
    def __init__(self, Inquilino_service:InquilinoService):
        """
        Construtor da classe InquilinoControl
        :param Inquilino_service: Instância do InquilinoService (injeção de dependência)
        """
        print("⬆️  InquilinoControl.constructor()")
        self.__Inquilino_service = Inquilino_service

    def store(self):
        """Cria um novo Inquilino"""
        print("🔵 InquilinoControle.store()")
       
        Inquilino_body_request = request.json.get("Inquilino")  #Pega os dados do Inquilino no corpo da requisição
        novo_id = self.__Inquilino_service.createInquilino(Inquilino_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "Inquilinos": [
                    {
                        "idInquilino": novo_id,
                        "nomeInquilino": Inquilino_body_request.get("nomeInquilino"),
                        "email": Inquilino_body_request.get("email"),
                        "telefone": Inquilino_body_request.get("telefone"),
                        "requisicao": Inquilino_body_request.get("requisicao"),
                        "cpf": Inquilino_body_request.get("cpf")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        """Lista todos os Inquilinos cadastrados"""
        print("🔵 InquilinoControle.index()")
       
        array_Inquilinos = self.__Inquilino_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"Inquilinos": array_Inquilinos}
        }), 200
        

    def show(self):
          # Pega o idInquilino diretamente da URI
        idInquilino = request.view_args.get("idInquilino")

        Inquilino = self.__Inquilino_service.findById(idInquilino)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"Inquilinos": Inquilino}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        """Atualiza os dados de um Inquilino existente"""
        print("🔵 InquilinoControle.update()")
       
        # Pega o idInquilino diretamente da URI
        idInquilino = request.view_args.get("idInquilino")

        # Pega os dados do Inquilino no corpo da requisição
        json_Inquilino = request.json.get("Inquilino")
        print(json_Inquilino)

        resposta = self.__Inquilino_service.updateInquilino(idInquilino, json_Inquilino)
        return jsonify({
            "success": True,
            "message": "Inquilino atualizado com sucesso",
            "data": {
                "Inquilino": {
                    "idInquilino": int(idInquilino),
                    "nomeInquilino": json_Inquilino.get("nomeInquilino")
                }
            }
        }), 200
   

    def destroy(self):
        """Remove um Inquilino pelo ID"""
        print("🔵 InquilinoControle.destroy()")
        # Pega o idInquilino diretamente da URI
        idInquilino = request.view_args.get("idInquilino")
        
        excluiu = self.__Inquilino_service.deleteInquilino(idInquilino)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Inquilino com id {idInquilino}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 200
        
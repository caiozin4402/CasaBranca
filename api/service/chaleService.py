# -*- coding: utf-8 -*-
from api.dao.chaleDAO import ChaleDAO
from api.modelo.chale import Chale
from api.utils.errorResponse import ErrorResponse

"""
Classe responsável pela camada de serviço para a entidade Chale.

Observações sobre injeção de dependência:
- O ChaleService recebe uma instância de ChaleDAO via construtor.
- Isso segue o padrão de injeção de dependência, tornando o serviço desacoplado
  do DAO concreto, facilitando testes unitários e substituição por mocks.
"""
class ChaleService:
    def __init__(self, Chale_dao_dependency: ChaleDAO):
        """
        Construtor da classe ChaleService

        :param Chale_dao_dependency: ChaleDAO - Instância de ChaleDAO
        """
        print("⬆️  ChaleService.__init__()")
        self.__ChaleDAO = Chale_dao_dependency  # injeção de dependência

    def createChale(self, ChaleBodyRequest: dict) -> int:
        """
        Cria um novo Chale.

        :param ChaleBodyRequest: dict - Dados do Chale {"nomeChale"}
        :return: int - ID do novo Chale criado

        🔹 Validações:
        - nomeChale não pode estar vazio
        - Não pode existir outro Chale com mesmo nome
        """
        print("🟣 ChaleService.createChale()")

        chale = Chale()
        chale.nome = ChaleBodyRequest.get("nome")
        chale.capacidade = ChaleBodyRequest.get("capacidade")


        # valida regra de negócio: Chale duplicado
        resultado = self.__ChaleDAO.findByField("nome", chale.nome)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Chale já existe",
                {"message": f"O Chale {chale.nome} já existe"}
            )

        return self.__ChaleDAO.create(chale)

    def findAll(self) -> list[dict]:
        """
        Retorna todos os Chales
        :return: list[dict]
        """
        print("🟣 ChaleService.findAll()")
        return self.__ChaleDAO.findAll()

    def findById(self, idChale: int) -> dict | None:
        """
        Retorna um Chale por ID.

        :param idChale: int
        :return: dict | None
        """
        print("🟣 ChaleService.findById()")

        chale = Chale()
        chale.idChale = idChale  # passa pela validação de domínio

        return self.__ChaleDAO.findById(chale.idChale)

    def updateChale(self, idChale: int, jsonChale: dict) -> bool:
        print (jsonChale)
        """
        Atualiza um Chale existente.

        🔹 Regra de domínio: o idChale deve ser um número inteiro positivo.

        :param idChale: int - Identificador do Chale a ser atualizado
        :param jsonChale: dict - Dados do Chale {"nomeChale", "email", "telefone", "requisicao", "cpf"}
        :return: bool - True se atualizado com sucesso
        :raises ValueError: se idChale ou nomeChale não atenderem às regras de domínio
        """
        print("🟣 ChaleService.updateChale()")

        chale = Chale()
        chale.idChale = idChale
        chale.nome = jsonChale.get("nome")
        chale.capacidade = jsonChale.get("capacidade")

        return self.__ChaleDAO.update(chale)

    def deleteChale(self, idChale: int) -> bool:
        """
        Deleta um Chale por ID.

        :param idChale: int
        :return: bool
        """
        print("🟣 ChaleService.deleteChale()")

        chale = Chale()
        chale.idChale = idChale  # validação de regra de domínio

        return self.__ChaleDAO.delete(chale)
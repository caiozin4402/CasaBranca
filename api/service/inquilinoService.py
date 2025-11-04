# -*- coding: utf-8 -*-
from api.dao.inquilinoDAO import InquilinoDAO
from api.modelo.inquilino import Inquilino
from api.utils.errorResponse import ErrorResponse

"""
Classe responsável pela camada de serviço para a entidade Inquilino.

Observações sobre injeção de dependência:
- O InquilinoService recebe uma instância de InquilinoDAO via construtor.
- Isso segue o padrão de injeção de dependência, tornando o serviço desacoplado
  do DAO concreto, facilitando testes unitários e substituição por mocks.
"""
class InquilinoService:
    def __init__(self, Inquilino_dao_dependency: InquilinoDAO):
        """
        Construtor da classe InquilinoService

        :param Inquilino_dao_dependency: InquilinoDAO - Instância de InquilinoDAO
        """
        print("⬆️  InquilinoService.__init__()")
        self.__InquilinoDAO = Inquilino_dao_dependency  # injeção de dependência

    def createInquilino(self, InquilinoBodyRequest: dict) -> int:
        """
        Cria um novo Inquilino.

        :param InquilinoBodyRequest: dict - Dados do Inquilino {"nomeInquilino"}
        :return: int - ID do novo Inquilino criado

        🔹 Validações:
        - nomeInquilino não pode estar vazio
        - Não pode existir outro Inquilino com mesmo nome
        """
        print("🟣 InquilinoService.createInquilino()")

        inquilino = Inquilino()
        inquilino.nomeInquilino = InquilinoBodyRequest.get("nomeInquilino")
        inquilino.email = InquilinoBodyRequest.get("email")
        inquilino.telefone = InquilinoBodyRequest.get("telefone")
        inquilino.requisicao = InquilinoBodyRequest.get("requisicao")
        inquilino.cpf = InquilinoBodyRequest.get("cpf")

        # valida regra de negócio: Inquilino duplicado
        resultado = self.__InquilinoDAO.findByField("nome", inquilino.nomeInquilino)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Inquilino já existe",
                {"message": f"O Inquilino {inquilino.nomeInquilino} já existe"}
            )

        return self.__InquilinoDAO.create(inquilino)

    def findAll(self) -> list[dict]:
        """
        Retorna todos os Inquilinos
        :return: list[dict]
        """
        print("🟣 InquilinoService.findAll()")
        return self.__InquilinoDAO.findAll()

    def findById(self, idInquilino: int) -> dict | None:
        """
        Retorna um Inquilino por ID.

        :param idInquilino: int
        :return: dict | None
        """
        print("🟣 InquilinoService.findById()")

        inquilino = Inquilino()
        inquilino.idInquilino = idInquilino  # passa pela validação de domínio

        return self.__InquilinoDAO.findById(inquilino.idInquilino)

    def updateInquilino(self, idInquilino: int, jsonInquilino: dict) -> bool:
        print (jsonInquilino)
        """
        Atualiza um Inquilino existente.

        🔹 Regra de domínio: o idInquilino deve ser um número inteiro positivo.

        :param idInquilino: int - Identificador do Inquilino a ser atualizado
        :param jsonInquilino: dict - Dados do Inquilino {"nomeInquilino", "email", "telefone", "requisicao", "cpf"}
        :return: bool - True se atualizado com sucesso
        :raises ValueError: se idInquilino ou nomeInquilino não atenderem às regras de domínio
        """
        print("🟣 InquilinoService.updateInquilino()")

        inquilino = Inquilino()
        inquilino.idInquilino = idInquilino
        inquilino.nomeInquilino = jsonInquilino.get("nomeInquilino")
        inquilino.email = jsonInquilino.get("email")
        inquilino.telefone = jsonInquilino.get("telefone")
        inquilino.requisicao = jsonInquilino.get("requisicao")
        inquilino.cpf = jsonInquilino.get("cpf")

        return self.__InquilinoDAO.update(inquilino)

    def deleteInquilino(self, idInquilino: int) -> bool:
        """
        Deleta um Inquilino por ID.

        :param idInquilino: int
        :return: bool
        """
        print("🟣 InquilinoService.deleteInquilino()")

        inquilino = Inquilino()
        inquilino.idInquilino = idInquilino  # validação de regra de domínio

        return self.__InquilinoDAO.delete(inquilino)
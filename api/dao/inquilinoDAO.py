# -*- coding: utf-8 -*-
from api.modelo.inquilino import Inquilino
from api.database.database import DatabaseConfig
"""
Representa o DAO (Data Access Object) de Inquilino.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Inquilino.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class InquilinoDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️  InquilinoDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objInquilino: Inquilino) -> int:
        SQL = "INSERT INTO inquilino (nome,email,telefone,requisicao,cpf) VALUES (%s,%s,%s,%s,%s);"
        params = (objInquilino.nomeInquilino,objInquilino.email,objInquilino.telefone,objInquilino.requisicao,objInquilino.cpf)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir Inquilino")
        print("✅ InquilinoDAO.create()")
        return insert_id

    def delete(self, Inquilino: Inquilino) -> bool:
        SQL = "DELETE FROM inquilino WHERE idInquilino = %s;"
        params = (Inquilino.idInquilino,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ InquilinoDAO.delete()")
        return affected > 0

    def update(self, objInquilino: Inquilino) -> bool:
        SQL = "UPDATE inquilino SET nome = %s, email = %s, telefone = %s, requisicao = %s, cpf = %s WHERE idInquilino = %s;"
        params = (objInquilino.nomeInquilino,objInquilino.email, objInquilino.telefone, objInquilino.requisicao, objInquilino.cpf, objInquilino.idInquilino)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ InquilinoDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM inquilino;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ InquilinoDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idInquilino: int) -> dict | None:
        resultados = self.findByField("idInquilino", idInquilino)
        print("✅ InquilinoDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idInquilino", "nome", "email", "telefone", "requisicao", "cpf"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM inquilino WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ InquilinoDAO.findByField()")
        return resultados
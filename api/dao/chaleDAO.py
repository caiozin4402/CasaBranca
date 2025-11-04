# -*- coding: utf-8 -*-
from api.modelo.chale import Chale
from api.database.database import DatabaseConfig

"""
Representa o DAO (Data Access Object) de Chale.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Chale.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class ChaleDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️  ChaleDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objChale: Chale) -> int:
        SQL = "INSERT INTO chale (nome,capacidade) VALUES (%s,%s);"
        params = (objChale.nome,objChale.capacidade)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir Chale")
        print("✅ ChaleDAO.create()")
        return insert_id

    def delete(self, Chale: Chale) -> bool:
        SQL = "DELETE FROM chale WHERE idChale = %s;"
        params = (Chale.idChale,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ ChaleDAO.delete()")
        return affected > 0

    def update(self, objChale: Chale) -> bool:
        SQL = "UPDATE Chale SET nome = %s, capacidade = %s WHERE idChale = %s;"
        params = (objChale.nome, objChale.capacidade, objChale.idChale)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ ChaleDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM chale;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ ChaleDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idChale: int) -> dict | None:
        resultados = self.findByField("idChale", idChale)
        print("✅ ChaleDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idChale", "nome", "capacidade"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM chale WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ ChaleDAO.findByField()")
        return resultados
# -*- coding: utf-8 -*-
from api.modelo.reserva import Reserva
from api.database.database import DatabaseConfig

"""
Representa o DAO (Data Access Object) de Reserva.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Reserva.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class ReservaDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️  ReservaDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objReserva: Reserva) -> int:
        SQL = "INSERT INTO reserva (idInquilino, idChale, inicio, fim) VALUES (%s, %s, %s, %s);"
        params = (objReserva.idInquilino, objReserva.idChale, objReserva.inicio, objReserva.fim)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir Reserva")
        print("✅ ReservaDAO.create()")
        return insert_id

    def delete(self, reserva: Reserva) -> bool:
        SQL = "DELETE FROM reserva WHERE idReserva = %s;"
        params = (reserva.idReserva,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ ReservaDAO.delete()")
        return affected > 0

    def update(self, objReserva: Reserva) -> bool:
        SQL = "UPDATE reserva SET idInquilino = %s, idChale = %s, inicio = %s, fim = %s WHERE idReserva = %s;"
        params = (objReserva.idInquilino, objReserva.idChale, objReserva.inicio, objReserva.fim, objReserva.idReserva)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ ReservaDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM reserva;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ ReservaDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idReserva: int) -> dict | None:
        resultados = self.findByField("idReserva", idReserva)
        print("✅ ReservaDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idReserva", "idInquilino", "idChale", "inicio", "fim"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM reserva WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ ReservaDAO.findByField()")
        return resultados
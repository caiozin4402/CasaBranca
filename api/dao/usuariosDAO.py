# -*- coding: utf-8 -*-
from api.modelo.usuarios import Usuario
from api.database.database import DatabaseConfig

class UsuarioDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        print("⬆️  UsuarioDAO.__init__()")
        self.__database = database_dependency

    def findByEmail(self, email: str) -> dict | None:
        """Busca usuário por email"""
        SQL = "SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE;"
        params = (email,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultado = cursor.fetchone()

        print(f"✅ UsuarioDAO.findByEmail() -> {'Encontrado' if resultado else 'Não encontrado'}")
        return resultado

    def create(self, usuario: Usuario) -> int:
        """Cria novo usuário"""
        SQL = "INSERT INTO usuarios (nome, email, senha, role, ativo) VALUES (%s, %s, %s, %s, %s);"
        params = (usuario.nome, usuario.email, usuario.senha, usuario.role, usuario.ativo)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir usuário")
        
        print("✅ UsuarioDAO.create()")
        return insert_id

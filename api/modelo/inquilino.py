import re
"""
Representa a entidade Inquilino do sistema.

Objetivo:
- Encapsular os dados de um inquilino.
- Garantir integridade dos atributos via getters e setters.
"""
class Inquilino:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        # Atributos privados de instância
        self.__idInquilino = None
        self.__nomeInquilino = None
        self.__email = None
        self.__telefone = None
        self.__requisicao = None
        self.__cpf = None

    @property
    def idInquilino(self):
        """
        Getter para idInquilino
        :return: int - Identificador do funcionário
        """
        return self.__idInquilino

    @idInquilino.setter
    def idInquilino(self, valor):
        """
        Define o ID do funcionário.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param valor: int - Número inteiro positivo representando o ID do funcionário.
        :raises ValueError: se não for número inteiro positivo.

        Exemplo:
        >>> f = Inquilino()
        >>> f.idInquilino = 10   # ✅ válido
        >>> f.idInquilino = -5   # ❌ lança erro
        """
        try:
            parsed = int(valor)
        except (ValueError, TypeError):
            raise ValueError("idInquilino deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idInquilino deve ser um número inteiro positivo.")

        self.__idInquilino = parsed

    @property
    def nomeInquilino(self):
        """
        Getter para nomeInquilino
        :return: str - Nome do funcionário
        """
        return self.__nomeInquilino

    @nomeInquilino.setter
    def nomeInquilino(self, value):
        """
        Define o nome do funcionário.

        🔹 Regra de domínio: deve ser string não vazia com pelo menos 3 caracteres.

        :param value: str - Nome do funcionário.
        :raises ValueError: se inválido.

        Exemplo:
        >>> f = Inquilino()
        >>> f.nomeInquilino = "João Silva"  # ✅ válido
        """
        if not isinstance(value, str):
            raise ValueError("nomeInquilino deve ser uma string.")

        nome = value.strip()

        if len(nome) < 3:
            raise ValueError("nomeInquilino deve ter pelo menos 3 caracteres.")

        self.__nomeInquilino = nome

    @property
    def email(self):
        """
        Getter para email
        :return: str - Email do funcionário
        """
        return self.__email

    @email.setter
    def email(self, value):
        """
        Define o email do funcionário.

        🔹 Regra de domínio: deve ser válido, não vazio e no formato correto.

        :param value: str - Email do funcionário.
        :raises ValueError: se inválido.
        """
        if not isinstance(value, str):
            raise ValueError("email deve ser uma string.")

        email_trimmed = value.strip()

        if email_trimmed == "":
            raise ValueError("email não pode ser vazio.")

        import re
        email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(email_regex, email_trimmed):
            raise ValueError("email em formato inválido.")

        self.__email = email_trimmed

    @property
    def telefone(self):
        """
        Getter para telefone
        :return: str - telefone do funcionário
        """
        return self.__telefone

    @telefone.setter
    def telefone(self, value):
        def validar_telefone(telefone):
            # Remove caracteres especiais e espaços
            numero = re.sub(r'[^0-9]', '', telefone)
            
            # Verifica o comprimento
            if len(numero) not in [10, 11]:
                return False
                
            # Verifica DDD (11-99)
            ddd = int(numero[:2])
            if ddd < 11 or ddd > 99:
                return False
                
            # Se for celular (11 dígitos), verifica se começa com 9
            if len(numero) == 11 and numero[2] != '9':
                return False
                
            return True
        
        if not validar_telefone(value):
            raise ValueError("telefone em formato inválido.")

        if not isinstance(value, str):
            raise ValueError("telefone deve ser uma string.")


        self.__telefone = value

    @property
    def requisicao(self):
        """
        Getter para recebeValeTransporte
        :return: int (0 ou 1)
        """
        return self.__requisicao

    @requisicao.setter
    def requisicao(self, value):
    
        self.__requisicao = value

    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, value):
        def validar_cpf(cpf):
            cpf = re.sub(r'[^0-9]', '', cpf)

            if len(cpf) != 11 or cpf == cpf[0] * 11:
                return False

            for i in range(9, 11):
                soma = sum(int(cpf[j]) * (i + 1 - j) for j in range(0, i))
                digito = (soma * 10 % 11) % 10
                if digito != int(cpf[i]):
                    return False

            return True

        if not validar_cpf(value):
            raise ValueError("CPF em formato inválido.")

        self.__cpf = value
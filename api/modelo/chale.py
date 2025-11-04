class Chale:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        # Atributos privados de instância
        self.__idChale = None
        self.__nome = None
        self.__capacidade = None
    
    @property
    def idChale(self):
        """
        Getter para idChale
        :return: int - Identificador do chalé
        """
        return self.__idChale
    @idChale.setter
    def idChale(self, valor):   
        try:
            parsed = int(valor)
        except (ValueError, TypeError):
            raise ValueError("idInquilino deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idInquilino deve ser um número inteiro positivo.")

        self.__idChale = parsed

    @property
    def nome(self):
        """
        Getter para nome
        :return: str - Nome do chalé
        """
        return self.__nome
    @nome.setter
    def nome(self, value):
        if not isinstance(value, str):
            raise ValueError("nomeInquilino deve ser uma string.")

        nome = value.strip()

        if len(nome) < 3:
            raise ValueError("nomeInquilino deve ter pelo menos 3 caracteres.")
        self.__nome = nome

    @property
    def capacidade(self):
        return self.__capacidade
    
    @capacidade.setter
    def capacidade(self, valor):
        try:
            capacidade = int(valor)
        except (ValueError, TypeError):
            raise ValueError("capacidade deve ser um número inteiro.")

        if capacidade <= 0:
            raise ValueError("capacidade deve ser um número inteiro positivo.")

        self.__capacidade = capacidade
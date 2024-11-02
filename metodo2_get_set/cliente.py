from decorador_de_tipagem import TipagemEstaticaClasse


@TipagemEstaticaClasse
class Cliente:
    def __init__(self, nome: str, telefone: str):
        self.__nome = nome.capitalize()
        self.__telefone = telefone

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not nome:
            raise ValueError("O nome não pode ser vazio")
        self.__nome = nome

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        if len(str(telefone)) != 11 or not telefone.isdigit():
            raise ValueError("O telefone deve conter 11 dígitos numéricos.")
        self.__telefone = telefone  # Telefone atualizado somente se válido

class Cliente:
    def __init__(self, nome_instancia: str, valor: str | None = None):
        self.__nome_instancia = nome_instancia
        self.__valor = valor

    def __get__(self, instance, outra) -> str:
        return self.__valor

    def __set__(self, instacia, valor):
        if instacia is None or not valor:
            raise ValueError(f"{self.__nome_instancia} não pode ser vazio.")
        self.__valor = valor

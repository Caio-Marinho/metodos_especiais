from decorador_de_tipagem import *


# Exemplo de uso
@TipagemEstaticaClasse
class Pessoa:
    def __init__(self, nome: str, idade: int, cidade: str):
        self.nome = nome
        self.idade = idade
        self.cidade = cidade

    def __str__(self) -> str:
        return f'Nome: {self.nome}, Idade: {self.idade},cidade:{self.cidade}'

    def novo_nome(self, nome: str):
        self.nome = nome
        return self.nome

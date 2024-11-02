from decorador_de_tipagem import TipagemEstaticaFunction
from aplicacao_tipagem import Pessoa


# Exemplo de uso
@TipagemEstaticaFunction  # Usar em uma função o decorador TipagemEstatica
def saudacao(nome: str, idade: int) -> str:
    return f"{nome} tem {idade}!"


# Testando o código
print(saudacao("Caio", 24))

pessoa: Pessoa = Pessoa('caio', 24, 'Recife')
print(pessoa)
pessoa.novo_nome('cio')
print(pessoa)

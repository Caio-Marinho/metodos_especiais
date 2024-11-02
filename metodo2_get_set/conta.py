from decorador_de_tipagem import TipagemEstaticaClasse


@TipagemEstaticaClasse
class Conta:
    def __init__(self, titular: str, numero: str):
        self.__titular = titular
        self.__numero = numero
        self.__saldo = 2500.00

    @property
    def saldo(self) -> float:
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo: float) -> None:
        if saldo < 0:
            raise ValueError("O saldo não pode ficar negativo")
        self.__saldo = saldo

    def saque(self, valor) -> str | ValueError:
        if valor > 0:
            self.saldo -= valor
            return f"Saque de {valor} realizado. Saldo atual: {self.__saldo}"
        else:
            raise ValueError("Informe um valor válido")

    def deposito(self, valor) -> str | ValueError:
        if valor >= 0:
            self.saldo = self.__saldo + valor
            return "Depósito de " + str(valor) + " realizado. Saldo atual: " + str(self.__saldo)
        else:
            raise ValueError("Informe um valor válido")

    def extrato(self):
        print("Nome Do Cliente:", self.__titular, "\nSaldo Atual Da Conta:%.2f" % self.saldo)

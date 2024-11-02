from metodo1_get_set.cliente import Cliente
from saldo import Saldo


class Conta:
    __nome = Cliente("nome")
    __telefone = Cliente("telefone")
    __saldo = Saldo()

    def __init__(self, nome: str, telefone: int, saldo: float = 2500.00):
        self.__nome = nome
        self.__telefone = telefone
        self.__saldo = saldo

    def __str__(self):
        return f"Conta(nome={self.__nome},Telefone={self.__telefone} saldo={self.__saldo})"

    def saque(self, valor):
        if valor <= 0:
            raise ValueError("Insira um valor válido para saque.")

        """if self.__saldo - valor < 0:
            valor_saque = self.__saldo  # Define valor máximo possível para o saque
            print("O valor solicitado excede o saldo disponível.")
            self.__saldo -= valor_saque
            print(f"Saque de {valor_saque} realizado. Saldo atual: {self.__saldo}")
        else:"""
        self.__saldo -= valor
        print(f"Saque de {valor} realizado. Saldo atual: {self.__saldo}")

    def deposito(self, valor):
        if valor <= 0:
            raise ValueError("Insira um valor válido para depósito.")
        self.__saldo += valor
        print(f"Depósito de {valor} realizado. Saldo atual: {self.__saldo}")

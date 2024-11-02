from pprint import pprint


class Saldo:
    def __get__(self, instance, owner):
        return instance.__saldo

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        instance.__saldo = value

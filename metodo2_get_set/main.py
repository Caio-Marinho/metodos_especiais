from cliente import Cliente
from conta import Conta

cliente = Cliente("caio", '81979056770')
conta = Conta(cliente.nome, cliente.telefone)
conta.extrato()
print(conta.saque(2000))
conta.extrato()
print(conta.saque(500))
conta.extrato()
print(conta.saque(500))
conta.extrato()

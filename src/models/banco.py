from cliente import Cliente
from conta import Conta

class Banco:
    def __init__(self):
        self.contas = []

        def criar_conta(self, nome, cpf, telefone):
            # Cria o cliente
            cliente = Cliente(nome, cpf, telefone)

            # Cria a conta vinculada ao cliente
            conta = Conta(cliente)

            # Adiciona a conta ao banco
            self.contas.append(conta)

            return conta

    def buscar_conta(self, numero):
        for conta in self.contas:
            if conta.numero_conta == numero:
                return conta
        
        return None

    def listar_contas(self):
        return list(self.contas)
from decimal import Decimal, InvalidOperation
from movimentacao import Movimentacao
from cliente import Cliente

class Conta:
    contas_criadas = 0
    
    def __init__(self, titular: Cliente, saldo = 0):
        Conta.contas_criadas += 1
    
        self.numero = Conta.contas_criadas
        self.titular = titular
        self.saldo = Decimal(str(saldo))
        self.movimentacoes = []

    @staticmethod
    def _validar_valor(valor):
        try:
            valor = Decimal(str(valor))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Valor inválido.")

        if not valor.is_finite() or valor <= 0:
            raise ValueError("O valor deve ser positivo e finito.")

        return valor

    def depositar(self, valor):
        valor = self._validar_valor(valor)

        self.saldo += valor

        self.movimentacoes.append(
            Movimentacao("Depósito", valor)
        )

    def sacar(self, valor):
        valor = self._validar_valor(valor)

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self.saldo -= valor
        self.movimentacoes.append(
            Movimentacao("Saque", valor)
        )

    def transferir(self, destino, valor, modelo):
        valor = self._validar_valor(valor)
        
        if not isinstance(destino, Conta):
            raise ValueError("Conta de destino inválida.")

        if destino is self:
            raise ValueError("Não é possível transferir para a mesma conta.")

        if not isinstance(modelo, str) or not modelo.strip():
            raise ValueError("Informe a modalidade da transferência.")

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        modalidade = modelo.strip().upper()

        self.saldo -= valor
        destino.saldo += valor

        self.movimentacoes.append(
            Movimentacao(f"Envio {modalidade}", valor)
        )
        destino.movimentacoes.append(
            Movimentacao(f"Recebido {modalidade}", valor)
        )
        return True
    
    def consultar_saldo(self):
        return self.saldo

    def consultar_extrato(self):
        return list(self.movimentacoes)

  
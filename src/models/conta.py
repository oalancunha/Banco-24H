import hashlib
import hmac
import os
from decimal import Decimal, InvalidOperation
from movimentacao import Movimentacao
from cliente import Cliente

class Conta:
    contas_criadas = 0
    TAMANHO_MINIMO_SENHA = 4
    _ITERACOES_HASH = 200_000

    def __init__(self, titular: Cliente, senha: str, saldo = 0):
        # Valida a senha ANTES de consumir um número de conta, para que uma
        # senha inválida não "queime" o número.
        self._validar_senha(senha)

        Conta.contas_criadas += 1

        self.numero = Conta.contas_criadas
        self.titular = titular
        self.saldo = Decimal(str(saldo))
        self.movimentacoes = []
        self.definir_senha(senha)

    # ------------------------------------------------------------------
    # Autenticação
    # ------------------------------------------------------------------
    @classmethod
    def _validar_senha(cls, senha):
        if not isinstance(senha, str) or len(senha) < cls.TAMANHO_MINIMO_SENHA:
            raise ValueError(
                f"A senha deve ter pelo menos {cls.TAMANHO_MINIMO_SENHA} caracteres."
            )

    @classmethod
    def _gerar_hash(cls, senha, salt):
        return hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), salt, cls._ITERACOES_HASH
        )

    def definir_senha(self, senha):
        """Guarda apenas o hash da senha (nunca o texto puro)."""
        self._validar_senha(senha)
        self._salt = os.urandom(16)
        self._senha_hash = self._gerar_hash(senha, self._salt)

    def possui_senha(self):
        # getattr: contas de um banco.pkl antigo não têm esses atributos
        return (
            getattr(self, "_salt", None) is not None
            and getattr(self, "_senha_hash", None) is not None
        )

    def verificar_senha(self, senha):
        if not self.possui_senha() or not isinstance(senha, str):
            return False
        return hmac.compare_digest(
            self._senha_hash, self._gerar_hash(senha, self._salt)
        )

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

  
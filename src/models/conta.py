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

        self.ID = Conta.contas_criadas
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
    def _validar_valor(valor_informado):
        """Único ponto de conversão do valor: recebe o que foi informado
        (texto como "10,50", int, float ou Decimal) e devolve um Decimal
        já validado (finito e positivo)."""
        if isinstance(valor_informado, str):
            valor_informado = valor_informado.strip().replace(",", ".")

        try:
            valor = Decimal(str(valor_informado))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Valor inválido.")

        if not valor.is_finite() or valor <= 0:
            raise ValueError("O valor deve ser positivo e finito.")

        return valor

    def depositar(self, valor_informado):
        valor = self._validar_valor(valor_informado)

        self.saldo += valor

        self.movimentacoes.append(
            Movimentacao("Depósito", valor)
        )

    def sacar(self, valor_informado):
        valor = self._validar_valor(valor_informado)

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self.saldo -= valor
        self.movimentacoes.append(
            Movimentacao("Saque", valor)
        )

    def transferir(self, destino, valor_informado, modelo, transferencia_id=None):
        valor = self._validar_valor(valor_informado)
        
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
            Movimentacao(
                f"Envio {modalidade}", valor, transferencia_id,
                self.ID, self.titular.nome, destino.ID, destino.titular.nome
            )
        )
        destino.movimentacoes.append(
            Movimentacao(
                f"Recebido {modalidade}", valor, transferencia_id,
                destino.ID, destino.titular.nome, self.ID, self.titular.nome
            )
        )
        return True
    
    def consultar_saldo(self):
        return self.saldo

    def consultar_extrato(self):
        return list(self.movimentacoes)

  
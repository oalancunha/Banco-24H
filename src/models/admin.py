import hashlib
import hmac
import os


class Admin:
    """Administrador pré-estabelecido do sistema (ID reservado: 0)."""

    ID = 0
    NOME = "Administrador"
    _ITERACOES_HASH = 200_000

    def __init__(self, senha="BancoRoot"):
        self.ID = self.ID
        self.nome = self.NOME
        self._salt = os.urandom(16)
        self._senha_hash = self._gerar_hash(senha, self._salt)

    @classmethod
    def _gerar_hash(cls, senha, salt):
        return hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), salt, cls._ITERACOES_HASH
        )

    def verificar_senha(self, senha):
        if not isinstance(senha, str):
            return False
        hash_informado = self._gerar_hash(senha, self._salt)
        return hmac.compare_digest(self._senha_hash, hash_informado)

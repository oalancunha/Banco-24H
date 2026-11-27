from datetime import datetime
from decimal import Decimal

class Movimentacao:
    def __init__(self, tipo: str, valor: Decimal, transferencia_id=None,
                 conta_id=None, conta_nome=None, contraparte_id=None,
                 contraparte_nome=None):
        self.tipo = tipo
        self.valor = Decimal(str(valor))
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.transferencia_id = transferencia_id
        self.conta_id = conta_id
        self.conta_nome = conta_nome
        self.contraparte_id = contraparte_id
        self.contraparte_nome = contraparte_nome

    def __str__(self):
        linha = f"{self.data_hora} | {self.tipo} | R$ {self.valor:.2f}"
        if getattr(self, "conta_id", None) is not None:
            linha += " | Remetente: {} (ID {})".format(
                getattr(self, "conta_nome", ""), getattr(self, "conta_id", ""))
        if getattr(self, "contraparte_id", None) is not None:
            linha += " | Destinatário: {} (ID {})".format(
                getattr(self, "contraparte_nome", ""),
                getattr(self, "contraparte_id", ""))
        return linha

    def __repr__(self):
        return self.__str__()

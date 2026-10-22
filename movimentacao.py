from datetime import datetime

class Movimentacao:

    def __init__(self, tipo: str, valor: float):
        self.tipo = tipo
        self.valor = valor
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return (
            f"{self.data_hora} | "
            f"{self.tipo} | "
            f"R$ {self.valor:.2f}"
        )

    def __repr__(self):
        return self.__str__()

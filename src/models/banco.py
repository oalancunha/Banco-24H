from cliente import Cliente
from conta import Conta


class Banco:
    def __init__(self):
        self.contas = []

    # ------------------------------------------------------------------
    # Métodos básicos (usados internamente)
    # ------------------------------------------------------------------
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
            if conta.numero == numero:
                return conta

        return None

    def listar_contas(self):
        return list(self.contas)

    # ------------------------------------------------------------------
    # Métodos usados pela interface (devolvem tuplas (resultado, mensagem))
    # ------------------------------------------------------------------
    def _obter_conta(self, numero):
        """Converte o texto digitado em inteiro e busca a conta."""
        try:
            return self.buscar_conta(int(numero))
        except (ValueError, TypeError):
            return None

    def cadastrar_cliente_e_criar_conta(self, nome, cpf, tel):
        conta = self.criar_conta(nome, cpf, tel)
        return True, f"Conta criada com sucesso! Número: {conta.numero}"

    def consultar_saldo(self, numero):
        conta = self._obter_conta(numero)
        if conta is None:
            return None, "Conta não encontrada."
        return conta.consultar_saldo(), ""

    def depositar(self, numero, valor):
        conta = self._obter_conta(numero)
        if conta is None:
            return False, "Conta não encontrada."
        try:
            conta.depositar(valor)
        except ValueError as erro:
            return False, str(erro)
        return True, "Depósito realizado com sucesso."

    def sacar(self, numero, valor):
        conta = self._obter_conta(numero)
        if conta is None:
            return False, "Conta não encontrada."
        try:
            conta.sacar(valor)
        except ValueError as erro:
            return False, str(erro)
        return True, "Saque autorizado."

    def transferir(self, origem, destino, valor, modalidade="TRANSFERÊNCIA"):
        conta_origem = self._obter_conta(origem)
        conta_destino = self._obter_conta(destino)
        if conta_origem is None or conta_destino is None:
            return False, "Conta de origem ou destino não encontrada."
        try:
            conta_origem.transferir(conta_destino, valor, modalidade)
        except ValueError as erro:
            return False, str(erro)
        return True, "Transferência realizada com sucesso."

    def obter_extrato_formatado(self, numero):
        conta = self._obter_conta(numero)
        if conta is None:
            return None, "Conta não encontrada."
        linhas = [str(m) for m in conta.consultar_extrato()]
        return "\n".join(linhas) or "Nenhuma movimentação.", ""
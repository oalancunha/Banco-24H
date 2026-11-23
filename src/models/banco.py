from cliente import Cliente
from conta import Conta


class Banco:
    def __init__(self):
        self.contas = []

    # ------------------------------------------------------------------
    # Métodos básicos (usados internamente)
    # ------------------------------------------------------------------
    def criar_conta(self, nome, cpf, telefone, senha):
        # Cria o cliente
        cliente = Cliente(nome, cpf, telefone)

        # Cria a conta vinculada ao cliente (valida a senha)
        conta = Conta(cliente, senha)

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

    def cadastrar_cliente_e_criar_conta(self, nome, cpf, tel, senha):
        try:
            conta = self.criar_conta(nome, cpf, tel, senha)
        except ValueError as erro:
            return False, str(erro)
        return True, f"Conta criada com sucesso! Número: {conta.numero}"

    def autenticar(self, numero, senha):
        """Valida número da conta + senha. Devolve (conta, mensagem)."""
        conta = self._obter_conta(numero)

        if conta is not None and not conta.possui_senha():
            return None, "Esta conta ainda não possui senha. Procure o gerente."

        # Mensagem única para conta inexistente OU senha errada, para não
        # revelar quais números de conta existem.
        if conta is None or not conta.verificar_senha(senha):
            return None, "Número da conta ou senha inválidos."

        return conta, ""

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
            return False, "Conta de destino não encontrada."
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
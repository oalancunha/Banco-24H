from decimal import Decimal
import re
from cliente import Cliente
from conta import Conta
from admin import Admin
from movimentacao import Movimentacao

class Banco:
    def __init__(self):
        self.contas = []
        self.admin = Admin()
        self.transferencias = []
        self.proximo_id_transferencia = 1

    @staticmethod
    def _normalizar_cpf(cpf):
        """Compara CPFs independentemente de pontos, traços ou espaços."""
        return re.sub(r"\D", "", str(cpf or ""))

    @classmethod
    def _cpf_valido(cls, cpf):
        """Valida os 11 dígitos e os dígitos verificadores do CPF."""
        numeros = cls._normalizar_cpf(cpf)
        if len(numeros) != 11 or numeros == numeros[0] * 11:
            return False
        valores = [int(n) for n in numeros]
        primeiro = (sum(valores[i] * (10 - i) for i in range(9)) * 10) % 11
        primeiro = 0 if primeiro == 10 else primeiro
        segundo = (sum(valores[i] * (11 - i) for i in range(10)) * 10) % 11
        segundo = 0 if segundo == 10 else segundo
        return valores[9] == primeiro and valores[10] == segundo

    @staticmethod
    def _telefone_valido(telefone):
        """Aceita telefone brasileiro com DDD e 8 ou 9 dígitos."""
        numeros = re.sub(r"\D", "", str(telefone or ""))
        if numeros.startswith("55") and len(numeros) in (12, 13):
            numeros = numeros[2:]
        if len(numeros) not in (10, 11):
            return False
        ddd = int(numeros[:2])
        numero = numeros[2:]
        if not 11 <= ddd <= 99:
            return False
        # Fixo: 8 dígitos começando de 2 a 5. Celular: 9 dígitos começando em 9.
        return (len(numero) == 8 and numero[0] in "2345") or (
            len(numero) == 9 and numero[0] == "9"
        )

    def _cpf_ja_cadastrado(self, cpf, ignorar_id=None):
        cpf_normalizado = self._normalizar_cpf(cpf)
        if not cpf_normalizado:
            return False
        return any(
            conta.ID != ignorar_id
            and self._normalizar_cpf(conta.titular.cpf) == cpf_normalizado
            for conta in self.contas
        )

    def criar_conta(self, nome, cpf, telefone, senha):
        if not self._cpf_valido(cpf):
            raise ValueError("CPF inválido. Informe os 11 dígitos e confira os dígitos verificadores.")
        if not self._telefone_valido(telefone):
            raise ValueError("Telefone inválido. Informe o DDD e um número com 8 ou 9 dígitos.")
        if self._cpf_ja_cadastrado(cpf):
            raise ValueError("Este CPF já está cadastrado em outra conta.")
        cliente = Cliente(nome, cpf, telefone)
        conta = Conta(cliente, senha)
        self.contas.append(conta)
        return conta

    def buscar_conta(self, ID):
        for conta in self.contas:
            if conta.ID == ID:
                return conta
        return None

    def listar_contas(self):
        return list(self.contas)

    def _obter_conta(self, ID):
        try:
            return self.buscar_conta(int(ID))
        except (ValueError, TypeError):
            return None

    def cadastrar_cliente_e_criar_conta(self, nome, cpf, tel, senha):
        try:
            conta = self.criar_conta(nome, cpf, tel, senha)
        except ValueError as erro:
            return False, str(erro)
        return True, f"Conta criada com sucesso! ID: {conta.ID}"

    def autenticar(self, ID, senha):
        try:
            id_informado = int(ID)
        except (ValueError, TypeError):
            id_informado = None
        if id_informado == 0:
            admin = getattr(self, "admin", None)
            if admin is not None and admin.verificar_senha(senha):
                return admin, ""
            return None, "ID da conta ou senha inválidos."
        conta = self._obter_conta(ID)
        if conta is not None and not conta.possui_senha():
            return None, "Esta conta ainda não possui senha. Procure o gerente."
        if conta is None or not conta.verificar_senha(senha):
            return None, "ID da conta ou senha inválidos."
        return conta, ""

    def consultar_saldo(self, ID):
        conta = self._obter_conta(ID)
        if conta is None:
            return None, "Conta não encontrada."
        return conta.consultar_saldo(), ""

    def depositar(self, ID, valor_informado):
        conta = self._obter_conta(ID)
        if conta is None:
            return False, "Conta não encontrada."
        try:
            conta.depositar(valor_informado)
        except ValueError as erro:
            return False, str(erro)
        return True, "Depósito realizado com sucesso."

    def sacar(self, ID, valor_informado):
        conta = self._obter_conta(ID)
        if conta is None:
            return False, "Conta não encontrada."
        try:
            conta.sacar(valor_informado)
        except ValueError as erro:
            return False, str(erro)
        return True, "Saque autorizado."

    def transferir(self, origem, destino, valor_informado, modalidade="TRANSFERÊNCIA"):
        conta_origem = self._obter_conta(origem)
        conta_destino = self._obter_conta(destino)
        if conta_origem is None or conta_destino is None:
            return False, "Conta de origem ou destino não encontrada."
        try:
            valor = Conta._validar_valor(valor_informado)
            if valor > conta_origem.saldo:
                raise ValueError("Saldo insuficiente.")
            if conta_origem is conta_destino:
                raise ValueError("Não é possível transferir para a mesma conta.")
            transferencia_id = getattr(self, "proximo_id_transferencia", 1)
            conta_origem.transferir(conta_destino, valor, modalidade, transferencia_id)
        except ValueError as erro:
            return False, str(erro)
        registro = {
            "id": transferencia_id, "origem_id": conta_origem.ID,
            "origem_nome": conta_origem.titular.nome,
            "destino_id": conta_destino.ID,
            "destino_nome": conta_destino.titular.nome,
            "valor": valor, "data_hora": conta_origem.movimentacoes[-1].data_hora,
            "modalidade": modalidade, "revertida": False,
        }
        if not hasattr(self, "transferencias"):
            self.transferencias = []
        self.transferencias.append(registro)
        self.proximo_id_transferencia = transferencia_id + 1
        return True, "Transferência realizada com sucesso."

    def migrar_transferencias_antigas(self):
        """Reconstrói o histórico anterior usando pares de envio/recebimento
        com mesmo valor e data/hora. Cada recebimento é usado uma única vez."""
        if not hasattr(self, "transferencias"):
            self.transferencias = []
        existentes = {t.get("id") for t in self.transferencias}
        recebimentos = []
        for conta in self.contas:
            for mov in conta.consultar_extrato():
                if str(getattr(mov, "tipo", "")).startswith("Recebido"):
                    recebimentos.append((conta, mov))
        proximo = max([0] + [int(i) for i in existentes if i is not None]) + 1
        for origem in self.contas:
            for envio in origem.consultar_extrato():
                if not str(getattr(envio, "tipo", "")).startswith("Envio"):
                    continue
                if getattr(envio, "transferencia_id", None) is not None:
                    continue
                par = next(((destino, receb) for destino, receb in recebimentos
                            if receb.valor == envio.valor
                            and receb.data_hora == envio.data_hora), None)
                if par is None:
                    continue
                destino, receb = par
                recebimentos.remove(par)
                envio.transferencia_id = proximo
                receb.transferencia_id = proximo
                envio.conta_id, envio.conta_nome = origem.ID, origem.titular.nome
                envio.contraparte_id, envio.contraparte_nome = destino.ID, destino.titular.nome
                receb.conta_id, receb.conta_nome = destino.ID, destino.titular.nome
                receb.contraparte_id, receb.contraparte_nome = origem.ID, origem.titular.nome
                self.transferencias.append({
                    "id": proximo, "origem_id": origem.ID,
                    "origem_nome": origem.titular.nome,
                    "destino_id": destino.ID, "destino_nome": destino.titular.nome,
                    "valor": envio.valor, "data_hora": envio.data_hora,
                    "modalidade": str(envio.tipo).replace("Envio ", ""),
                    "revertida": False,
                })
                proximo += 1
        self.proximo_id_transferencia = max(
            getattr(self, "proximo_id_transferencia", 1), proximo)

    def listar_transferencias(self):
        return list(getattr(self, "transferencias", []))

    def reverter_transferencia(self, transferencia_id):
        try:
            transferencia_id = int(transferencia_id)
        except (ValueError, TypeError):
            return False, "Identificador de transferência inválido."
        registro = next((t for t in self.listar_transferencias() if t["id"] == transferencia_id), None)
        if registro is None:
            return False, "Transferência não encontrada."
        if registro.get("revertida", False):
            return False, "Esta transferência já foi revertida."
        origem = self.buscar_conta(registro["origem_id"])
        destino = self.buscar_conta(registro["destino_id"])
        if origem is None or destino is None:
            return False, "Não foi possível localizar as duas contas da transferência."
        valor = Decimal(str(registro["valor"]))
        if destino.saldo < valor:
            return False, "A conta receptora não possui saldo suficiente para devolver o valor integral."
        destino.saldo -= valor
        origem.saldo += valor
        destino.movimentacoes.append(Movimentacao(
            "Estorno de transferência enviada", valor, transferencia_id,
            destino.ID, destino.titular.nome, origem.ID, origem.titular.nome))
        origem.movimentacoes.append(Movimentacao(
            "Estorno de transferência recebida", valor, transferencia_id,
            origem.ID, origem.titular.nome, destino.ID, destino.titular.nome))
        registro["revertida"] = True
        registro["data_reversao"] = destino.movimentacoes[-1].data_hora
        return True, "Transferência revertida com sucesso."

    def alterar_dados_usuario(self, ID, nome, cpf, telefone, nova_senha=None):
        conta = self._obter_conta(ID)
        if conta is None:
            return False, "Conta não encontrada."
        if not nome.strip() or not cpf.strip() or not telefone.strip():
            return False, "Nome, CPF e telefone são obrigatórios."
        if not self._cpf_valido(cpf):
            return False, "CPF inválido. Informe os 11 dígitos e confira os dígitos verificadores."
        if not self._telefone_valido(telefone):
            return False, "Telefone inválido. Informe o DDD e um número com 8 ou 9 dígitos."
        if self._cpf_ja_cadastrado(cpf, ignorar_id=conta.ID):
            return False, "Este CPF já está cadastrado em outra conta."
        if nova_senha:
            try:
                Conta._validar_senha(nova_senha)
            except ValueError as erro:
                return False, str(erro)
        conta.titular.nome = nome.strip()
        conta.titular.cpf = cpf.strip()
        conta.titular.telefone = telefone.strip()
        if nova_senha:
            conta.definir_senha(nova_senha)
        return True, "Dados do usuário atualizados com sucesso."

    def encerrar_conta(self, ID):
        conta = self._obter_conta(ID)
        if conta is None:
            return False, "Conta não encontrada."
        if conta.saldo != Decimal("0"):
            return False, "A conta só pode ser encerrada quando o saldo for R$ 0,00."
        self.contas.remove(conta)
        return True, "Conta encerrada com sucesso."

    def obter_extrato_formatado(self, ID):
        conta = self._obter_conta(ID)
        if conta is None:
            return None, "Conta não encontrada."
        linhas = [str(m) for m in conta.consultar_extrato()]
        return "\n".join(linhas) or "Nenhuma movimentação.", ""

import tkinter as tk
from tkinter import ttk, messagebox

class InterfaceBanco24H:
    def __init__(self, root, backend_banco):
        """
        Recebe a instância do backend (regras de negócio) criada por outro integrante.
        """
        self.banco = backend_banco
        self.root = root
        self.root.title("Sistema Caixa 24h")
        self.root.geometry("750x600")
        self.root.configure(bg="#f4f6f9")

        # Estilização
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f4f6f9")
        self.style.configure("TNotebook", background="#f4f6f9")
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[10, 5])

        # Cabeçalho Principal
        header = tk.Frame(self.root, bg="#102a43", height=60)
        header.pack(fill="x", side="top")
        tk.Label(
            header, 
            text="SISTEMA CAIXA 24H", 
            font=("Helvetica", 16, "bold"), 
            fg="white", 
            bg="#102a43"
        ).pack(pady=15)

        # Abas da Aplicação
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Construção das telas conforme Casos de Uso
        self._criar_aba_gerente()      # Cadastrar Cliente e Criar Conta
        self._criar_aba_operacoes()    # Consultar Saldo, Depósito, Saque
        self._criar_aba_transferencia()# Realizar Transferência
        self._criar_aba_extrato()      # Exibir Extrato

    # --------------------------------------------------------------------------
    # 1. PERFIL GERENTE: CADASTRAR CLIENTE E CRIAR CONTA
    # --------------------------------------------------------------------------
    def _criar_aba_gerente(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Área do Gerente ")

        box = tk.LabelFrame(aba, text=" Cadastrar Cliente e Criar Conta ", font=("Helvetica", 11, "bold"), bg="white", padx=20, pady=20)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        # Campos solicitados no diagrama (nome, cpf, tel)
        tk.Label(box, text="Nome Completo:", bg="white").grid(row=0, column=0, sticky="w", pady=8)
        self.ent_nome = tk.Entry(box, width=35)
        self.ent_nome.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(box, text="CPF:", bg="white").grid(row=1, column=0, sticky="w", pady=8)
        self.ent_cpf = tk.Entry(box, width=35)
        self.ent_cpf.grid(row=1, column=1, pady=8, padx=5)

        tk.Label(box, text="Telefone:", bg="white").grid(row=2, column=0, sticky="w", pady=8)
        self.ent_tel = tk.Entry(box, width=35)
        self.ent_tel.grid(row=2, column=1, pady=8, padx=5)

        btn = tk.Button(box, text="Cadastrar e Abrir Conta", bg="#2b6cb0", fg="white", font=("Helvetica", 10, "bold"), command=self._exec_cadastrar_cliente)
        btn.grid(row=3, column=0, columnspan=2, pady=20)

    # --------------------------------------------------------------------------
    # 2. PERFIL CLIENTE: SALDO, DEPÓSITO E SAQUE
    # --------------------------------------------------------------------------
    def _criar_aba_operacoes(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Operações ")

        box = tk.LabelFrame(aba, text=" Caixas Eletrônicos (Cliente) ", font=("Helvetica", 11, "bold"), bg="white", padx=20, pady=20)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(box, text="Número da Conta:", bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.ent_num_conta = tk.Entry(box, width=25)
        self.ent_num_conta.grid(row=0, column=1, pady=10, padx=5)

        tk.Label(box, text="Valor (R$):", bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.ent_valor_op = tk.Entry(box, width=25)
        self.ent_valor_op.grid(row=1, column=1, pady=10, padx=5)

        btn_area = tk.Frame(box, bg="white")
        btn_area.grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(btn_area, text="Consultar Saldo", bg="#319795", fg="white", width=14, font=("Helvetica", 9, "bold"), command=self._exec_consultar_saldo).pack(side="left", padx=5)
        tk.Button(btn_area, text="Realizar Depósito", bg="#2f855a", fg="white", width=14, font=("Helvetica", 9, "bold"), command=self._exec_depositar).pack(side="left", padx=5)
        tk.Button(btn_area, text="Realizar Saque", bg="#c53030", fg="white", width=14, font=("Helvetica", 9, "bold"), command=self._exec_sacar).pack(side="left", padx=5)

    # --------------------------------------------------------------------------
    # 3. PERFIL CLIENTE: TRANSFERÊNCIA
    # --------------------------------------------------------------------------
    def _criar_aba_transferencia(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Transferência ")

        box = tk.LabelFrame(aba, text=" Transferir Valor ", font=("Helvetica", 11, "bold"), bg="white", padx=20, pady=20)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(box, text="Conta Origem:", bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.ent_tr_origem = tk.Entry(box, width=25)
        self.ent_tr_origem.grid(row=0, column=1, pady=10, padx=5)

        tk.Label(box, text="Conta Destino:", bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.ent_tr_destino = tk.Entry(box, width=25)
        self.ent_tr_destino.grid(row=1, column=1, pady=10, padx=5)

        tk.Label(box, text="Valor (R$):", bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.ent_tr_valor = tk.Entry(box, width=25)
        self.ent_tr_valor.grid(row=2, column=1, pady=10, padx=5)

        tk.Button(box, text="Confirmar Transferência", bg="#dd6b20", fg="white", font=("Helvetica", 10, "bold"), command=self._exec_transferir).grid(row=3, column=0, columnspan=2, pady=20)

    # --------------------------------------------------------------------------
    # 4. PERFIL CLIENTE: EXIBIR EXTRATO
    # --------------------------------------------------------------------------
    def _criar_aba_extrato(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Extrato ")

        box = tk.Frame(aba, bg="white", padx=10, pady=10)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        top = tk.Frame(box, bg="white")
        top.pack(fill="x", pady=5)

        tk.Label(top, text="Número da Conta:", bg="white").pack(side="left", padx=5)
        self.ent_extrato_conta = tk.Entry(top, width=15)
        self.ent_extrato_conta.pack(side="left", padx=5)

        tk.Button(top, text="Exibir Extrato", bg="#2b6cb0", fg="white", font=("Helvetica", 9, "bold"), command=self._exec_exibir_extrato).pack(side="left", padx=5)

        self.txt_extrato = tk.Text(box, height=15, width=60, font=("Consolas", 10))
        self.txt_extrato.pack(fill="both", expand=True, pady=10)

    # ==========================================================================
    # LÓGICA DE VALIDAÇÃO E CHAMADAS AO BACKEND
    # ==========================================================================
    def _validar_float(self, val_str):
        try:
            v = float(val_str.replace(",", "."))
            return v if v > 0 else None
        except ValueError:
            return None

    def _exec_cadastrar_cliente(self):
        nome = self.ent_nome.get().strip()
        cpf = self.ent_cpf.get().strip()
        tel = self.ent_tel.get().strip()

        if not nome or not cpf or not tel:
            messagebox.showerror("Erro de Validação", "Todos os campos (nome, cpf, tel) são obrigatórios!")
            return

        # Chama a regra de negócio do backend
        sucesso, msg = self.banco.cadastrar_cliente_e_criar_conta(nome, cpf, tel)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.ent_nome.delete(0, tk.END)
            self.ent_cpf.delete(0, tk.END)
            self.ent_tel.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", msg)

    def _exec_consultar_saldo(self):
        num = self.ent_num_conta.get().strip()
        if not num:
            messagebox.showerror("Erro", "Informe o número da conta!")
            return
        
        saldo, msg = self.banco.consultar_saldo(num)
        if saldo is not None:
            messagebox.showinfo("Saldo", f"Saldo atual da conta {num}: R$ {saldo:.2f}")
        else:
            messagebox.showerror("Erro", msg)

    def _exec_depositar(self):
        num = self.ent_num_conta.get().strip()
        valor = self._validar_float(self.ent_valor_op.get().strip())

        if not num or valor is None:
            messagebox.showerror("Erro", "Informe uma conta válida e um valor positivo!")
            return

        sucesso, msg = self.banco.depositar(num, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.ent_valor_op.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", msg)

    def _exec_sacar(self):
        num = self.ent_num_conta.get().strip()
        valor = self._validar_float(self.ent_valor_op.get().strip())

        if not num or valor is None:
            messagebox.showerror("Erro", "Informe uma conta válida e um valor positivo!")
            return

        # Chamada ao método sacar(valor)
        sucesso, msg = self.banco.sacar(num, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", msg) # 'Saque Autorizado'
            self.ent_valor_op.delete(0, tk.END)
        else:
            messagebox.showerror("Erro de Saque", msg)

    def _exec_transferir(self):
        origem = self.ent_tr_origem.get().strip()
        destino = self.ent_tr_destino.get().strip()
        valor = self._validar_float(self.ent_tr_valor.get().strip())

        if not origem or not destino or valor is None:
            messagebox.showerror("Erro", "Preencha as duas contas e um valor válido!")
            return

        sucesso, msg = self.banco.transferir(origem, destino, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.ent_tr_valor.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", msg)

    def _exec_exibir_extrato(self):
        num = self.ent_extrato_conta.get().strip()
        if not num:
            messagebox.showerror("Erro", "Informe o número da conta!")
            return

        # Obtém os dados e renderiza o bloco
        texto_extrato, msg = self.banco.obter_extrato_formatado(num)
        self.txt_extrato.delete("1.0", tk.END)

        if texto_extrato is not None:
            self.txt_extrato.insert(tk.END, texto_extrato)
        else:
            messagebox.showerror("Erro", msg)

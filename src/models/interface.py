import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

COR_FUNDO = "#f4f6f9"
COR_HEADER = "#102a43"


class InterfaceBanco24H:
    def __init__(self, root, backend_banco):
        """
        Recebe a instância do backend (regras de negócio) criada por outro integrante.
        """
        self.banco = backend_banco
        self.root = root
        self.conta_logada = None  # sessão: conta autenticada (None = ninguém logado)

        self.root.title("Sistema Caixa 24h")
        self.root.geometry("750x600")
        self.root.configure(bg=COR_FUNDO)

        # Estilização
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=COR_FUNDO)
        self.style.configure("TNotebook", background=COR_FUNDO)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[10, 5])

        # Cabeçalho Principal
        header = tk.Frame(self.root, bg=COR_HEADER, height=60)
        header.pack(fill="x", side="top")
        tk.Label(
            header,
            text="SISTEMA CAIXA 24H",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg=COR_HEADER
        ).pack(pady=15)

        # Identificação do usuário logado + botão Sair (só aparece após o login)
        self.frm_usuario = tk.Frame(header, bg=COR_HEADER)
        self.lbl_usuario = tk.Label(
            self.frm_usuario, text="", font=("Helvetica", 9), fg="white", bg=COR_HEADER
        )
        self.lbl_usuario.pack(side="left", padx=8)
        tk.Button(
            self.frm_usuario, text="Sair", bg="#c53030", fg="white",
            font=("Helvetica", 9, "bold"), command=self._exec_logout
        ).pack(side="left")

        # Área de conteúdo: troca entre "tela de login" e "sistema" conforme a sessão
        self.container = tk.Frame(self.root, bg=COR_FUNDO)
        self.container.pack(fill="both", expand=True)

        self._mostrar_login()

    # --------------------------------------------------------------------------
    # CONTROLE DE TELAS (LOGIN <-> SISTEMA)
    # --------------------------------------------------------------------------
    def _limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def _mostrar_login(self):
        self._limpar_container()
        self.frm_usuario.place_forget()

        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self._criar_aba_login()     # Entrar com número da conta + senha
        self._criar_aba_gerente()   # Cadastrar Cliente e Criar Conta

        self.ent_login_conta.focus_set()

    def _mostrar_sistema(self):
        self._limpar_container()

        self.lbl_usuario.config(
            text=f"Conta {self.conta_logada.numero} - {self.conta_logada.titular.nome}"
        )
        self.frm_usuario.place(relx=1.0, rely=0.5, anchor="e", x=-15)

        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Telas do cliente logado (nenhuma pede número de conta)
        self._criar_aba_operacoes()     # Consultar Saldo, Depósito, Saque
        self._criar_aba_transferencia() # Realizar Transferência
        self._criar_aba_conta()         # Dados cadastrais, saldo e acesso ao extrato

    # --------------------------------------------------------------------------
    # 0. LOGIN
    # --------------------------------------------------------------------------
    def _criar_aba_login(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Entrar ")

        box = tk.LabelFrame(aba, text=" Acesso do Cliente ", font=("Helvetica", 11, "bold"), bg="white", padx=20, pady=20)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(box, text="ID:", bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.ent_login_conta = tk.Entry(box, width=25)
        self.ent_login_conta.grid(row=0, column=1, pady=10, padx=5)

        tk.Label(box, text="Senha:", bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.ent_login_senha = tk.Entry(box, width=25, show="*")
        self.ent_login_senha.grid(row=1, column=1, pady=10, padx=5)

        tk.Button(box, text="Entrar", bg="#2b6cb0", fg="white", width=14, font=("Helvetica", 10, "bold"), command=self._exec_login).grid(row=2, column=0, columnspan=2, pady=20)

        # Enter também confirma o login
        self.ent_login_conta.bind("<Return>", self._exec_login)
        self.ent_login_senha.bind("<Return>", self._exec_login)

    # --------------------------------------------------------------------------
    # 1. PERFIL GERENTE: CADASTRAR CLIENTE E CRIAR CONTA
    # --------------------------------------------------------------------------
    def _criar_aba_gerente(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Cadastro ")

        box = tk.LabelFrame(aba, text=" Cadastrar Cliente e Criar Conta ", font=("Helvetica", 11, "bold"), bg="white", padx=20, pady=20)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        # Campos solicitados no diagrama (nome, cpf, tel) + senha de acesso
        tk.Label(box, text="Nome Completo:", bg="white").grid(row=0, column=0, sticky="w", pady=8)
        self.ent_nome = tk.Entry(box, width=35)
        self.ent_nome.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(box, text="CPF:", bg="white").grid(row=1, column=0, sticky="w", pady=8)
        self.ent_cpf = tk.Entry(box, width=35)
        self.ent_cpf.grid(row=1, column=1, pady=8, padx=5)

        tk.Label(box, text="Telefone:", bg="white").grid(row=2, column=0, sticky="w", pady=8)
        self.ent_tel = tk.Entry(box, width=35)
        self.ent_tel.grid(row=2, column=1, pady=8, padx=5)

        tk.Label(box, text="Senha:", bg="white").grid(row=3, column=0, sticky="w", pady=8)
        self.ent_senha_cadastro = tk.Entry(box, width=35, show="*")
        self.ent_senha_cadastro.grid(row=3, column=1, pady=8, padx=5)

        tk.Label(box, text="Confirmar Senha:", bg="white").grid(row=4, column=0, sticky="w", pady=8)
        self.ent_senha_confirma = tk.Entry(box, width=35, show="*")
        self.ent_senha_confirma.grid(row=4, column=1, pady=8, padx=5)

        btn = tk.Button(box, text="Cadastrar e Abrir Conta", bg="#2b6cb0", fg="white", font=("Helvetica", 10, "bold"), command=self._exec_cadastrar_cliente)
        btn.grid(row=5, column=0, columnspan=2, pady=20)

    # --------------------------------------------------------------------------
    # 2. PERFIL CLIENTE: SALDO, DEPÓSITO E SAQUE
    # --------------------------------------------------------------------------
    def _criar_aba_operacoes(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Operações ")

        box = tk.LabelFrame(aba, text=" Caixa Eletrônico ", font=("Helvetica", 11, "bold"), bg="white", padx=20, pady=20)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(box, text="Valor (R$):", bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.ent_valor_op = tk.Entry(box, width=25)
        self.ent_valor_op.grid(row=0, column=1, pady=10, padx=5)

        btn_area = tk.Frame(box, bg="white")
        btn_area.grid(row=1, column=0, columnspan=2, pady=20)

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

        tk.Label(box, text="Conta Destino (ID):", bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.ent_tr_destino = tk.Entry(box, width=25)
        self.ent_tr_destino.grid(row=1, column=1, pady=10, padx=5)

        tk.Label(box, text="Valor (R$):", bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.ent_tr_valor = tk.Entry(box, width=25)
        self.ent_tr_valor.grid(row=2, column=1, pady=10, padx=5)

        tk.Button(box, text="Confirmar Transferência", bg="#dd6b20", fg="white", font=("Helvetica", 10, "bold"), command=self._exec_transferir).grid(row=3, column=0, columnspan=2, pady=20)

    # --------------------------------------------------------------------------
    # 4. PERFIL CLIENTE: CONTA
    # --------------------------------------------------------------------------
    def _criar_aba_conta(self):
        aba = ttk.Frame(self.notebook)
        self.notebook.add(aba, text=" Conta ")

        box = tk.LabelFrame(
            aba, text=" Informações da Conta ", font=("Helvetica", 11, "bold"),
            bg="white", padx=25, pady=20
        )
        box.pack(fill="both", expand=True, padx=15, pady=15)

        conta = self.conta_logada
        dados = (
            ("Titular:", conta.titular.nome),
            ("CPF:", conta.titular.cpf),
            ("Telefone:", conta.titular.telefone),
            ("Número da conta:", str(conta.numero)),
        )
        for linha, (rotulo, valor) in enumerate(dados):
            tk.Label(
                box, text=rotulo, bg="white",
                font=("Helvetica", 10, "bold")
            ).grid(row=linha, column=0, sticky="w", pady=9, padx=(0, 15))
            tk.Label(
                box, text=valor, bg="white", font=("Helvetica", 10)
            ).grid(row=linha, column=1, sticky="w", pady=9)

        tk.Label(
            box, text="Saldo disponível:", bg="white",
            font=("Helvetica", 11, "bold")
        ).grid(row=4, column=0, sticky="w", pady=(20, 10), padx=(0, 15))

        self.lbl_saldo_conta = tk.Label(
            box, text="", bg="white", fg="#2f855a",
            font=("Helvetica", 15, "bold")
        )
        self.lbl_saldo_conta.grid(row=4, column=1, sticky="w", pady=(20, 10))
        self._atualizar_saldo_conta()

        tk.Button(
            box, text="Extrato", bg="#2b6cb0", fg="white",
            font=("Helvetica", 10, "bold"), width=16,
            command=self._abrir_tela_extrato
        ).grid(row=5, column=0, columnspan=2, pady=25)

    def _atualizar_saldo_conta(self):
        if hasattr(self, "lbl_saldo_conta") and self.conta_logada is not None:
            self.lbl_saldo_conta.config(
                text=f"R$ {self.conta_logada.consultar_saldo():.2f}"
            )

    def _abrir_tela_extrato(self):
        janela = tk.Toplevel(self.root)
        janela.title("Extrato da Conta")
        janela.geometry("650x450")
        janela.configure(bg=COR_FUNDO)
        janela.transient(self.root)

        box = tk.Frame(janela, bg="white", padx=15, pady=15)
        box.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            box, text="Extrato da Conta", bg="white",
            font=("Helvetica", 13, "bold")
        ).pack(anchor="w", pady=(0, 10))

        area = tk.Frame(box, bg="white")
        area.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(area)
        scrollbar.pack(side="right", fill="y")

        texto = tk.Text(
            area, font=("Consolas", 10), wrap="none",
            yscrollcommand=scrollbar.set, state="normal"
        )
        texto.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=texto.yview)

        # Mais recente primeiro (ordem cronológica decrescente).
        movimentacoes = sorted(
            self.conta_logada.consultar_extrato(),
            key=lambda mov: datetime.strptime(
                mov.data_hora, "%d/%m/%Y %H:%M:%S"
            ),
            reverse=True
        )

        if movimentacoes:
            texto.insert("1.0", "\n".join(str(mov) for mov in movimentacoes))
        else:
            texto.insert("1.0", "Nenhuma movimentação.")
        texto.config(state="disabled")

    # ==========================================================================
    # LÓGICA DE VALIDAÇÃO E CHAMADAS AO BACKEND
    # ==========================================================================
    def _validar_float(self, val_str):
        try:
            v = float(val_str.replace(",", "."))
            return v if v > 0 else None
        except ValueError:
            return None

    def _exec_login(self, event=None):
        num = self.ent_login_conta.get().strip()
        senha = self.ent_login_senha.get()

        if not num or not senha:
            messagebox.showerror("Erro", "Informe o número da conta e a senha!")
            return

        conta, msg = self.banco.autenticar(num, senha)
        if conta is None:
            self.ent_login_senha.delete(0, tk.END)
            messagebox.showerror("Falha no login", msg)
            return

        self.conta_logada = conta
        self._mostrar_sistema()

    def _exec_logout(self):
        self.conta_logada = None
        self._mostrar_login()

    def _exec_cadastrar_cliente(self):
        nome = self.ent_nome.get().strip()
        cpf = self.ent_cpf.get().strip()
        tel = self.ent_tel.get().strip()
        senha = self.ent_senha_cadastro.get()
        confirma = self.ent_senha_confirma.get()

        if not nome or not cpf or not tel or not senha:
            messagebox.showerror("Erro de Validação", "Todos os campos (nome, cpf, tel, senha) são obrigatórios!")
            return

        if senha != confirma:
            messagebox.showerror("Erro de Validação", "A senha e a confirmação não conferem!")
            return

        # Chama a regra de negócio do backend
        sucesso, msg = self.banco.cadastrar_cliente_e_criar_conta(nome, cpf, tel, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            for campo in (self.ent_nome, self.ent_cpf, self.ent_tel,
                          self.ent_senha_cadastro, self.ent_senha_confirma):
                campo.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", msg)

    def _exec_consultar_saldo(self):
        num = self.conta_logada.numero

        saldo, msg = self.banco.consultar_saldo(num)
        if saldo is not None:
            messagebox.showinfo("Saldo", f"Saldo atual da conta {num}: R$ {saldo:.2f}")
        else:
            messagebox.showerror("Erro", msg)

    def _exec_depositar(self):
        valor = self._validar_float(self.ent_valor_op.get().strip())

        if valor is None:
            messagebox.showerror("Erro", "Informe um valor positivo!")
            return

        sucesso, msg = self.banco.depositar(self.conta_logada.numero, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.ent_valor_op.delete(0, tk.END)
            self._atualizar_saldo_conta()
        else:
            messagebox.showerror("Erro", msg)

    def _exec_sacar(self):
        valor = self._validar_float(self.ent_valor_op.get().strip())

        if valor is None:
            messagebox.showerror("Erro", "Informe um valor positivo!")
            return

        # Chamada ao método sacar(valor)
        sucesso, msg = self.banco.sacar(self.conta_logada.numero, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", msg) # 'Saque Autorizado'
            self.ent_valor_op.delete(0, tk.END)
            self._atualizar_saldo_conta()
        else:
            messagebox.showerror("Erro de Saque", msg)

    def _exec_transferir(self):
        origem = self.conta_logada.numero
        destino = self.ent_tr_destino.get().strip()
        valor = self._validar_float(self.ent_tr_valor.get().strip())

        if not destino or valor is None:
            messagebox.showerror("Erro", "Informe a conta de destino e um valor válido!")
            return

        sucesso, msg = self.banco.transferir(origem, destino, valor)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.ent_tr_valor.delete(0, tk.END)
            self._atualizar_saldo_conta()
        else:
            messagebox.showerror("Erro", msg)

    def _exec_exibir_extrato(self):
        # Obtém os dados e renderiza o bloco
        texto_extrato, msg = self.banco.obter_extrato_formatado(self.conta_logada.numero)
        self.txt_extrato.delete("1.0", tk.END)

        if texto_extrato is not None:
            self.txt_extrato.insert(tk.END, texto_extrato)
        else:
            messagebox.showerror("Erro", msg)

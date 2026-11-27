import os
import pickle
import tkinter as tk  # Import necessário para o Tkinter

from banco import Banco
from conta import Conta
from admin import Admin
from interface import InterfaceBanco24H  # Importa a sua classe de interface

ARQUIVO = "banco.pkl"


def salvar_banco(banco):
    """Grava o banco em um arquivo temporário e depois substitui o original,
    evitando que o banco.pkl fique corrompido se a gravação for interrompida."""
    temp = ARQUIVO + ".tmp"
    with open(temp, "wb") as arquivo:
        pickle.dump(banco, arquivo)
    os.replace(temp, ARQUIVO)


def carregar_banco():
    """Lê o banco.pkl; se não existir (ou estiver vazio), cria um novo."""
    if os.path.exists(ARQUIVO) and os.path.getsize(ARQUIVO) > 0:
        with open(ARQUIVO, "rb") as arquivo:
            banco = pickle.load(arquivo)
    else:
        banco = Banco()
        salvar_banco(banco)

    # Compatibilidade com banco.pkl criado antes da inclusão do administrador.
    # O administrador não é armazenado na lista de contas dos clientes.
    if not hasattr(banco, "admin"):
        banco.admin = Admin()

    # Recupera também transferências antigas, anteriores ao registro global.
    banco.migrar_transferencias_antigas()

    # O contador é atributo de classe e não vai no pickle:
    # restaura a partir do maior número de conta existente.
    contas = banco.listar_contas()
    if contas:
        Conta.contas_criadas = max(
            (conta.ID for conta in contas),
            default=0,
        )
    return banco


def main():
    banco = None
    try:
        banco = carregar_banco()

        # --- INTEGRAÇÃO COM A INTERFACE GRÁFICA ---
        root = tk.Tk()  # Cria a janela principal do Tkinter
        app = InterfaceBanco24H(root, banco)  # Instancia a interface passando o banco carregado
        root.mainloop()  # Inicia o loop de execução da janela

    finally:
        # Executa sempre: fim normal, exceção ou fechamento da janela
        if banco is not None:
            salvar_banco(banco)
            print("Dados salvos em banco.pkl.")


if __name__ == "__main__":
    main()
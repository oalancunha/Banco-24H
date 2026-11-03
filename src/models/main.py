import os
import pickle

from banco import Banco
from conta import Conta

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

    # O contador é atributo de classe e não vai no pickle:
    # restaura a partir do maior número de conta existente.
    Conta.contas_criadas = max(
        (conta.numero for conta in banco.listar_contas()),
        default=0,
    )
    return banco


def main():
    banco = None
    try:
        banco = carregar_banco()

        # O programa roda aqui
        print(f"Contas carregadas: {len(banco.listar_contas())}")
        conta = banco.criar_conta("Ana", "12345678900", "11999999999")
        conta.depositar(500)

    finally:
        # Executa sempre: fim normal, exceção ou Ctrl+C
        if banco is not None:
            salvar_banco(banco)
            print("Dados salvos em banco.pkl.")


if __name__ == "__main__":
    main()
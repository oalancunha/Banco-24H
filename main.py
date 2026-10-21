from conta import Conta
from cliente import Cliente

ana = Cliente("Ana", "12345678900", "11999999999")
bruno = Cliente("Bruno", "98765432100", "11888888888")

conta_ana = Conta(ana)
conta_bruno = Conta(bruno)

conta_ana.depositar(500)
conta_ana.sacar(100)
conta_ana.transferir(conta_bruno, 150, "PIX")

print(f"Saldo da Ana: R$ {conta_ana.consultar_saldo():.2f}")
print(f"Saldo do Bruno: R$ {conta_bruno.consultar_saldo():.2f}")

print("\n--- Extrato da Ana ---")
for movimentacao in conta_ana.consultar_extrato():
    print(movimentacao)

print("\n--- Extrato do Bruno ---")
for movimentacao in conta_bruno.consultar_extrato():
    print(movimentacao)


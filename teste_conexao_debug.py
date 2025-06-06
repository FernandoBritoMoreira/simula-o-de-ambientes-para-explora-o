import sim
import time

print("Encerrando conexões anteriores...")
sim.simxFinish(-1)

print("Tentando conectar ao CoppeliaSim na porta 19997...")
client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if client_id != -1:
    print(f"✅ Conectado com sucesso! client_id = {client_id}")
    sim.simxFinish(client_id)
else:
    print("❌ Falha ao conectar! Verifique se:")
    print(" - O CoppeliaSim está aberto.")
    print(" - A simulação está rodando (botão Play).")
    print(" - A porta 19997 está ativa (Remote API).")

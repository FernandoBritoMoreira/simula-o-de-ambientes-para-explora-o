import sim
import time
import struct

print("Encerrando conexões anteriores...")
sim.simxFinish(-1)

print("Conectando ao CoppeliaSim...")
client_id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if client_id != -1:
    print("✅ Conectado!")

    print("Lendo sinal Hokuyo...")
    sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_streaming)
    time.sleep(1)

    while True:
        _, data = sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_buffer)
        if data:
            distances = struct.unpack(f'{len(data)//4}f', data)
            print(f"✅ Dados recebidos: {len(distances)} distâncias")
            break
        else:
            print("⏳ Esperando dados...")
            time.sleep(0.5)

    sim.simxFinish(client_id)
else:
    print("❌ Falha na conexão.")

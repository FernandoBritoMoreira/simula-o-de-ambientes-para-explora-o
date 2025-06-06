import sim
import struct

def ler_hokuyo(client_id):
    _, dados = sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_buffer)
    if _ == sim.simx_return_ok and dados:
        dados = struct.unpack('f' * (len(dados) // 4), dados)
        return list(dados)
    else:
        print("[AVISO] Dados do Hokuyo não recebidos corretamente.")
        return []
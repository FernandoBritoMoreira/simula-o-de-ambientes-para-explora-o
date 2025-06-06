import sim

def ler_dados_hokuyo(client_id):
    err, signal = sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_blocking)
    if err == sim.simx_return_ok and signal:
        return sim.simxUnpackFloats(signal)
    return []

def obter_posicao_robo(client_id, robo_handle):
    err, pos = sim.simxGetObjectPosition(client_id, robo_handle, -1, sim.simx_opmode_blocking)
    if err == 0:
        return pos[0], pos[1]
    return 0, 0

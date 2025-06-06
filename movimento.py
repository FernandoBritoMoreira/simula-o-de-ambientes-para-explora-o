import sim

NOMES_MOTORES = [
    'joint_front_left_wheel',
    'joint_back_left_wheel',
    'joint_front_right_wheel',
    'joint_back_right_wheel'
]

def obter_handles_motores(client_id):
    handles = []
    for nome in NOMES_MOTORES:
        erro, handle = sim.simxGetObjectHandle(client_id, nome, sim.simx_opmode_blocking)
        if erro != sim.simx_return_ok:
            raise Exception(f"❌ Erro ao obter handle do motor {nome}.")
        handles.append(handle)
    return handles

def mover_frente(client_id, motores):
    v = 2.0
    for i in [0, 1]:
        sim.simxSetJointTargetVelocity(client_id, motores[i], v, sim.simx_opmode_streaming)
    for i in [2, 3]:
        sim.simxSetJointTargetVelocity(client_id, motores[i], -v, sim.simx_opmode_streaming)

def girar_direita(client_id, motores):
    v = 1.5
    for i in [0, 1]:
        sim.simxSetJointTargetVelocity(client_id, motores[i], v, sim.simx_opmode_streaming)
    for i in [2, 3]:
        sim.simxSetJointTargetVelocity(client_id, motores[i], v, sim.simx_opmode_streaming)

def girar_esquerda(client_id, motores):
    v = 1.5
    for i in [0, 1]:
        sim.simxSetJointTargetVelocity(client_id, motores[i], -v, sim.simx_opmode_streaming)
    for i in [2, 3]:
        sim.simxSetJointTargetVelocity(client_id, motores[i], -v, sim.simx_opmode_streaming)

def parar_robo(client_id, motores):
    for m in motores:
        sim.simxSetJointTargetVelocity(client_id, m, 0, sim.simx_opmode_streaming)
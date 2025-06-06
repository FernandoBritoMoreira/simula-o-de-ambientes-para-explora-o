import sim
import time
from mapa import atualizar_mapa, mostrar_mapa, decidir_acao
from movimento import mover_frente, girar_direita, girar_esquerda, parar_robo
from odometria import obter_posicao_robo

def conectar():
    sim.simxFinish(-1)
    client_id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
    if client_id != -1:
        print("\u2705 Conectado ao CoppeliaSim!")
    else:
        raise Exception("\u274C Falha ao conectar ao CoppeliaSim.")
    return client_id

def obter_handles_motores(client_id):
    nomes = [
        'joint_back_left_wheel',
        'joint_front_left_wheel',
        'joint_back_right_wheel',
        'joint_front_right_wheel'
    ]
    motores = []
    for nome in nomes:
        err, handle = sim.simxGetObjectHandle(client_id, nome, sim.simx_opmode_blocking)
        if err != 0:
            raise Exception(f"[ERRO] N\u00e3o foi poss\u00edvel obter handle de {nome}")
        motores.append(handle)
    return motores

def obter_handle_robo(client_id):
    err, robo_handle = sim.simxGetObjectHandle(client_id, 'Robotnik_Summit_XL', sim.simx_opmode_blocking)
    if err != 0:
        raise Exception("\u274C N\u00e3o foi poss\u00edvel obter o handle do rob\u00f4.")
    return robo_handle

def ler_hokuyo(client_id):
    err, data = sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_buffer)
    if err == sim.simx_return_ok and data:
        return list(sim.simxUnpackFloats(data))
    return []

def controlar(client_id, motores, robo_handle):
    mapa = None
    sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_streaming)
    time.sleep(0.2)

    while True:
        posicao_robo = obter_posicao_robo(client_id, robo_handle)
        distancias = ler_hokuyo(client_id)

        if mapa is None:
            from mapa import mapa as mapa_base
            mapa = mapa_base

        acao = decidir_acao(distancias)

        if acao == 'girar_esquerda':
            girar_esquerda(client_id, motores)
        elif acao == 'girar_direita':
            girar_direita(client_id, motores)
        elif acao == 'parar':
            parar_robo(client_id, motores)
        else:
            mover_frente(client_id, motores)
            atualizar_mapa(mapa, distancias, posicao_robo)  # ← atualiza só aqui

        mostrar_mapa(mapa, posicao_robo)
        time.sleep(0.1)


def main():
    client_id = conectar()
    motores = obter_handles_motores(client_id)
    robo = obter_handle_robo(client_id)
    controlar(client_id, motores, robo)

if __name__ == "__main__":
    main()
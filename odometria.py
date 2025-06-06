import sim
import math

def obter_posicao_robo(client_id, robo_handle):
    _, pos = sim.simxGetObjectPosition(client_id, robo_handle, -1, sim.simx_opmode_blocking)
    _, ori = sim.simxGetObjectOrientation(client_id, robo_handle, -1, sim.simx_opmode_blocking)
    x = pos[0]
    y = pos[1]
    theta = ori[2]
    return (x, y, theta)

import numpy as np
import matplotlib.pyplot as plt
import math

TAMANHO_MAPA_METROS = (40, 40)
ESCALA = 10
TAMANHO_MAPA = (TAMANHO_MAPA_METROS[0] * ESCALA, TAMANHO_MAPA_METROS[1] * ESCALA)
mapa = np.zeros(TAMANHO_MAPA, dtype=np.uint8)
centro_x = TAMANHO_MAPA[0] // 2
centro_y = TAMANHO_MAPA[1] // 2

def bresenham(x0, y0, x1, y1):
    """Retorna os pontos da linha entre (x0, y0) e (x1, y1) usando o algoritmo de Bresenham."""
    pontos = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            pontos.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            pontos.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    pontos.append((x1, y1))
    return pontos

def atualizar_mapa(mapa, distancias, posicao_robo):
    x_robo, y_robo, theta = posicao_robo
    x_robo_mapa = int(centro_x + x_robo * ESCALA)
    y_robo_mapa = int(centro_y - y_robo * ESCALA)

    for i, distancia in enumerate(distancias):
        if distancia <= 0 or distancia >= 4.9:
            continue

        angulo = -135 + i * 0.3515625
        rad = math.radians(angulo)

        x_rel = math.cos(rad) * distancia
        y_rel = math.sin(rad) * distancia

        x_rot = math.cos(theta) * x_rel - math.sin(theta) * y_rel
        y_rot = math.sin(theta) * x_rel + math.cos(theta) * y_rel

        x_abs = x_robo + x_rot
        y_abs = y_robo + y_rot

        x_mapa = int(centro_x + x_abs * ESCALA)
        y_mapa = int(centro_y - y_abs * ESCALA)

        if not (0 <= x_mapa < TAMANHO_MAPA[0] and 0 <= y_mapa < TAMANHO_MAPA[1]):
            continue

        # Traça linha do robô até o ponto: marca como LIVRE, exceto se já for obstáculo forte
        pontos_linha = bresenham(x_robo_mapa, y_robo_mapa, x_mapa, y_mapa)
        for ponto in pontos_linha[:-1]:
            px, py = ponto
            if 0 <= px < TAMANHO_MAPA[0] and 0 <= py < TAMANHO_MAPA[1]:
                if mapa[py, px] < 150:  # só modifica se ainda não for obstáculo forte
                    mapa[py, px] = max(mapa[py, px] - 1, 10)

        # Marca o último ponto como OBSTÁCULO se ainda não for um obstáculo fixo
        if 0 <= x_mapa < TAMANHO_MAPA[0] and 0 <= y_mapa < TAMANHO_MAPA[1]:
            if mapa[y_mapa, x_mapa] < 150:
                mapa[y_mapa, x_mapa] = min(mapa[y_mapa, x_mapa] + 3, 200)



def mostrar_mapa(mapa, posicao_robo):
    plt.clf()
    plt.imshow(mapa, cmap='gray')

    x_robo = int(centro_x + posicao_robo[0] * ESCALA)
    y_robo = int(centro_y - posicao_robo[1] * ESCALA)
    theta = posicao_robo[2]

    plt.plot(x_robo, y_robo, 'ro')  # ponto do robô

    # desenha seta com orientação
    dx = 10 * math.cos(theta)
    dy = -10 * math.sin(theta)
    plt.arrow(x_robo, y_robo, dx, dy, head_width=3, head_length=5, color='red')

    plt.pause(0.001)

def decidir_acao(distancias, distancia_minima=1.5):
    frente = distancias[280:400]
    esquerda = distancias[500:630]   # Setor da esquerda
    direita = distancias[50:180]     # Setor da direita

    obstaculo_frente = any(d < distancia_minima for d in frente if d > 0)
    obstaculo_esquerda = any(d < distancia_minima for d in esquerda if d > 0)
    obstaculo_direita = any(d < distancia_minima for d in direita if d > 0)

    if obstaculo_frente:
        # Desvia para o lado mais livre
        media_esq = sum([d for d in esquerda if d > 0]) / len([d for d in esquerda if d > 0])
        media_dir = sum([d for d in direita if d > 0]) / len([d for d in direita if d > 0])
        return 'girar_esquerda' if media_esq > media_dir else 'girar_direita'

    if obstaculo_esquerda and not obstaculo_direita:
        return 'girar_direita'
    elif obstaculo_direita and not obstaculo_esquerda:
        return 'girar_esquerda'

    return 'seguir'
import random


def transformar_duas_listas_em_set(lista_1, lista_2):
    set_1 = set(lista_1)
    set_2 = set(lista_2)
    set_final = set_1.union(set_2)
    return set_final


def restaurar_estado_inicial_celulas(lista_celulas):
    for celula in lista_celulas:
        celula.restaurar_estado_inicial()


def obter_matriz_manual(linhas, colunas):
    grid = []

    for y in range(linhas):
        linha = [0]*colunas
        grid.append(linha)

    return grid


def obter_matriz_randomica(qnt_linhas, qnt_colunas, pesos=(90, 10)):

    matriz = []

    escolhas = [0, 1]

    for y in range(qnt_linhas):
        linha = random.choices(escolhas, weights=pesos, k=qnt_colunas)
        matriz.append(linha)

    return matriz


def converter_pos_para_coordenada_grid(tupla_pos, tamanho_celula):
    pos_grid = tuple(map(lambda x: int(x / tamanho_celula), tupla_pos))
    return pos_grid


def obter_distancia(pos_grid_inicial, pos_grid_final, custo_menor_mov=10, custo_maior_mov=14):

    dx = abs(pos_grid_final[0] - pos_grid_inicial[0])
    dy = abs(pos_grid_final[1] - pos_grid_inicial[1])

    if dx > dy:
        distancia = custo_maior_mov * dy + custo_menor_mov * (dx - dy)
    else:
        distancia = custo_maior_mov * dx + custo_menor_mov * (dy - dx)

    return distancia

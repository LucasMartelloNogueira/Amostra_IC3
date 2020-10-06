from ClasseCelulaV4 import CelulaGridV4
import funcoes_auxiliares as func_aux
import pygame as pg
import cores


class GridAStar:

    def __init__(self, qnt_linhas, qnt_colunas, cell_size, matriz_layout):

        self.qnt_linhas = qnt_linhas
        self.qnt_colunas = qnt_colunas
        self.cell_size = cell_size
        self.largura = qnt_colunas * cell_size
        self.altura = qnt_linhas * cell_size
        self.custo_menor_mov = 10
        self.custo_maior_mov = 14
        self.matriz_nodulos = []

        for y in range(qnt_linhas):
            linha = []
            for x in range(qnt_colunas):
                andavel = True
                if matriz_layout[y][x] != 0:
                    andavel = False
                novo_nodulo = CelulaGridV4(x, y, andavel)
                linha.append(novo_nodulo)

            self.matriz_nodulos.append(linha)

        self.nodulo_partida = None
        self.nodulo_partida_selecionado = False
        self.nodulo_chegada = None
        self.nodulo_chegada_selecionado = False
        self.permissao_mudar_estado = True
        self.partida_e_chegada_definidos = False
        self.visualizar_a_star = False

        self.display_linhas_grid = True

    def update_grid(self, janela: pg.display):

        for linha in self.matriz_nodulos:
            for nodulo in linha:

                pg.draw.rect(janela, nodulo.cor, (nodulo.grid_x * self.cell_size, nodulo.grid_y * self.cell_size,
                                                  self.cell_size, self.cell_size))
        if self.display_linhas_grid is True:

            for x in range(self.qnt_colunas):
                pg.draw.line(janela, cores.preto, (x * self.cell_size, 0), (x * self.cell_size, self.altura), 1)

            for y in range(self.qnt_linhas):
                pg.draw.line(janela, cores.preto, (0, y * self.cell_size), (self.largura, y * self.cell_size), 1)

    def selecinar_nodulo(self, pos_nodulo_clicado):
        pos_x, pos_y = pos_nodulo_clicado[0], pos_nodulo_clicado[1]
        nodulo_selecionado = self.matriz_nodulos[pos_y][pos_x]

        return nodulo_selecionado

    def obter_nodulos_vizinhos(self, nodulo):

        lista_vizinhos = []

        for y in range(-1, 2):
            for x in range(-1, 2):

                pos_x = nodulo.grid_x + x
                pos_y = nodulo.grid_y + y

                if (pos_x, pos_y) == nodulo.pos_grid:
                    continue
                else:
                    if 0 <= pos_x <= self.qnt_colunas - 1:
                        if 0 <= pos_y <= self.qnt_linhas - 1:
                            nodulo_analisado = self.matriz_nodulos[pos_y][pos_x]
                            if nodulo_analisado.andavel is True:
                                lista_vizinhos.append(nodulo_analisado)
        return lista_vizinhos

    def selecionar_nodulo_partida(self, celula_selecionada):
        self.nodulo_partida = celula_selecionada
        self.nodulo_partida_selecionado = True
        self.permissao_mudar_estado = False
        celula_selecionada.cor = cores.verde

    def selecionar_celula_chegada(self, celula_selecionada):
        self.nodulo_chegada = celula_selecionada
        self.nodulo_chegada_selecionado = True
        self.permissao_mudar_estado = False
        celula_selecionada.cor = cores.vermelho

    def display_vizinhos(self, janela: pg.display, lista_vizinhos, cor=cores.azul):

        for vizinho in lista_vizinhos:
            pg.draw.rect(janela, cor, (vizinho.grid_x * self.cell_size, vizinho.grid_y * self.cell_size,
                                       self.cell_size, self.cell_size))

    def a_star(self, nodulo_inicial, nodulo_final):

        nodulo_inicial.g = 0
        nodulo_inicial.atualizar_h(nodulo_final.pos_grid)
        nodulo_inicial.atualizar_f()
        nodulo_inicial.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(nodulo_inicial)

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta[0]      # obtendo o nodulo de menor f

            for nodulo in lista_aberta:
                if nodulo.f < nodulo_atual.f or nodulo.f == nodulo_atual.f and nodulo.h < nodulo_atual.h:
                    nodulo_atual = nodulo

            lista_aberta.remove(nodulo_atual)
            lista_fechada.append(nodulo_atual)

            if nodulo_atual == nodulo_final:

                lista_bruta = [i.pos_grid for i in lista_fechada]
                lista_refinada = []

                nodulo_regresso = nodulo_final

                while nodulo_regresso != nodulo_inicial:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_final = (lista_bruta, lista_refinada)

                self.mudar_cor_celulas_procura_caminho(lista_bruta)
                self.mudar_cor_celulas_caminho(lista_refinada)

                lista_celulas_usadas = func_aux.transformar_duas_listas_em_set(lista_aberta, lista_fechada)
                func_aux.restaurar_estado_inicial_celulas(lista_celulas_usadas)

                self.visualizar_a_star = True

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g()
                    vizinho.atualizar_h(nodulo_final.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                if vizinho.andavel is False or vizinho in lista_fechada:
                    continue

                distacia_vizinho = func_aux.obter_distancia(nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                if novo_mov_para_vizinho < vizinho.g or vizinho not in lista_aberta:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho not in lista_aberta:
                        lista_aberta.append(vizinho)

        return None

    def a_star_v2(self, nodulo_inicial, nodulo_final):

        nodulo_inicial.g = 0
        nodulo_inicial.atualizar_h(nodulo_final.pos_grid)
        nodulo_inicial.atualizar_f()
        nodulo_inicial.ja_foi_visitado = True

        lista_aberta = []
        lista_fechada = []
        lista_aberta.append(nodulo_inicial)

        while len(lista_aberta) > 0:

            nodulo_atual = lista_aberta.pop(0)  # obtendo o nodulo de menor f
            nodulo_atual.ja_foi_analisado = True
            lista_fechada.append(nodulo_atual)

            if nodulo_atual == nodulo_final:

                lista_bruta = [i.pos_grid for i in lista_fechada]
                lista_refinada = []

                nodulo_regresso = nodulo_final

                while nodulo_regresso != nodulo_inicial:
                    lista_refinada.insert(0, nodulo_regresso.pos_grid)
                    nodulo_regresso = nodulo_regresso.parente

                lista_final = (lista_bruta, lista_refinada)

                self.mudar_cor_celulas_procura_caminho(lista_bruta)
                self.mudar_cor_celulas_caminho(lista_refinada)

                lista_celulas_usadas = func_aux.transformar_duas_listas_em_set(lista_aberta, lista_fechada)
                func_aux.restaurar_estado_inicial_celulas(lista_celulas_usadas)
                self.visualizar_a_star = True

                return lista_final

            lista_nodulos_vizinhos = self.obter_nodulos_vizinhos(nodulo_atual)

            for vizinho in lista_nodulos_vizinhos:

                if vizinho.andavel is False or vizinho.ja_foi_analisado is True:
                    continue

                if vizinho.ja_foi_visitado is False:
                    vizinho.parente = nodulo_atual
                    vizinho.atualizar_g()
                    vizinho.atualizar_h(nodulo_final.pos_grid)
                    vizinho.atualizar_f()
                    vizinho.ja_foi_visitado = True

                distacia_vizinho = func_aux.obter_distancia(nodulo_atual.pos_grid, vizinho.pos_grid)
                novo_mov_para_vizinho = nodulo_atual.g + distacia_vizinho

                vizinho_na_lista_aberta = False

                if vizinho in lista_aberta:
                    vizinho_na_lista_aberta = True

                if novo_mov_para_vizinho < vizinho.g or vizinho_na_lista_aberta is False:
                    vizinho.g = novo_mov_para_vizinho
                    vizinho.atualizar_f()
                    vizinho.parente = nodulo_atual
                    if vizinho_na_lista_aberta is False:
                        if len(lista_aberta) == 0:
                            lista_aberta.append(vizinho)
                        else:
                            for i in range(len(lista_aberta)):
                                if vizinho.f < lista_aberta[i].f:
                                    lista_aberta.insert(i, vizinho)
                                    break
                                elif vizinho.f == lista_aberta[i].f and vizinho.h < lista_aberta[i].h:
                                    lista_aberta.insert(i, vizinho)
                                    break
                                elif i == len(lista_aberta) - 1:
                                    lista_aberta.append(vizinho)

        return None

    def mudar_cor_celulas_procura_caminho(self, lista_coordenadas, cor=cores.roxo):
        for coordenada in lista_coordenadas:
            if (coordenada == self.nodulo_partida.pos_grid) or (coordenada == self.nodulo_chegada.pos_grid):
                continue
            else:
                x, y = coordenada[0], coordenada[1]
                celula_analisada = self.matriz_nodulos[y][x]
                celula_analisada.cor = cor

    def mudar_cor_celulas_caminho(self, lista_coordenadas, cor=cores.azul):
        for coordenada in lista_coordenadas:
            if (coordenada == self.nodulo_partida.pos_grid) or (coordenada == self.nodulo_chegada.pos_grid):
                continue
            else:
                x, y = coordenada[0], coordenada[1]
                celula_analisada = self.matriz_nodulos[y][x]
                celula_analisada.cor = cor

    def resetar_a_star(self):
        self.nodulo_partida = None
        self.nodulo_partida_selecionado = False
        self.nodulo_chegada = None
        self.nodulo_chegada_selecionado = False
        self.partida_e_chegada_definidos = False
        self.visualizar_a_star = False

        for linha in self.matriz_nodulos:
            for nodulo in linha:
                if nodulo.andavel is True:
                    nodulo.cor = cores.branco
                else:
                    nodulo.cor = cores.preto

    def display_procura_caminho(self, lista, janela: pg.display, cor=cores.roxo):
        for passo in lista:
            x = passo[0]
            y = passo[1]
            pg.draw.rect(janela, cor, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

    def display_menor_caminho(self, lista, janela: pg.display, cor=cores.azul):
        for passo in lista:
            x = passo[0]
            y = passo[1]
            pg.draw.rect(janela, cor, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

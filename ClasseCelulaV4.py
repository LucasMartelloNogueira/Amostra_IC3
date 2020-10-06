import cores
import funcoes_auxiliares as func_aux


class CelulaGridV4:

    def __init__(self, grid_x, grid_y, andavel=True, parente=None, g=0, h=0, f=0):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_grid = (grid_x, grid_y)
        self.andavel = andavel
        self.parente = parente
        self.ja_foi_visitado = False
        self.ja_foi_analisado = False
        self.g = g
        self.h = h
        self.f = f
        if andavel is True:
            self.cor = cores.branco
        else:
            self.cor = cores.preto

    def mudar_estado(self):

        if self.andavel is True:
            self.andavel = False
            self.cor = cores.preto
        else:
            self.andavel = True
            self.cor = cores.branco

    def atualizar_g(self):
        self.g = self.parente.g + func_aux.obter_distancia(self.parente.pos_grid, self.pos_grid)

    def atualizar_h(self, pos_grid_final):
        self.h = func_aux.obter_distancia(self.pos_grid, pos_grid_final)

    def atualizar_f(self):
        self.f = self.g + self.h

    def restaurar_estado_inicial(self):
        self.parente = None
        self.ja_foi_visitado = False
        self.ja_foi_analisado = False
        self.g = 0
        self.h = 0
        self.f = 0

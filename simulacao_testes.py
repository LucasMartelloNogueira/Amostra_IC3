import pygame
import funcoes_auxiliares as func_aux
from ClasseGridAStar import GridAStar
import time


def main():

    #  INFO GRID
    qnt_linhas = 100
    qnt_colunas = 100
    tamanho_celula = 6

    matriz_randomica = True

    if matriz_randomica is False:
        matriz = func_aux.obter_matriz_manual(qnt_linhas, qnt_colunas)
    else:
        matriz = func_aux.obter_matriz_randomica(qnt_linhas, qnt_colunas)

    grid = GridAStar(qnt_linhas, qnt_colunas, tamanho_celula, matriz)
    grid.display_linhas_grid = False

    janela = pygame.display.set_mode((grid.largura, grid.altura))
    pygame.display.set_caption('testes A*')
    pygame.init()

    comecar = False
    a_star_utilizado = 2
    mainloop = True

    while mainloop is True:

        grid.update_grid(janela)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if grid.visualizar_a_star is True:
                        grid.resetar_a_star()

                    pos_mouse = pygame.mouse.get_pos()
                    pos_mouse_grid = func_aux.converter_pos_para_coordenada_grid(pos_mouse, grid.cell_size)
                    nodulo_selecionado = grid.selecinar_nodulo(pos_mouse_grid)

                    if grid.partida_e_chegada_definidos is False:

                        if grid.nodulo_partida_selecionado is False and grid.permissao_mudar_estado is True:
                            grid.selecionar_nodulo_partida(nodulo_selecionado)

                        if grid.nodulo_chegada_selecionado is False and grid.permissao_mudar_estado is True:
                            grid.selecionar_celula_chegada(nodulo_selecionado)
                    else:
                        nodulo_selecionado.mudar_estado()

            if event.type == pygame.MOUSEBUTTONUP:
                grid.permissao_mudar_estado = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    comecar = True

                if event.key == pygame.K_1:
                    a_star_utilizado = 1
                    print("mudou para o A* tipo 1, sem optimizacao heap")

                if event.key == pygame.K_2:
                    a_star_utilizado = 2
                    print("mudou para o A* tipo 2, com optimizacao heap")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    comecar = False

        if grid.nodulo_partida_selecionado is True and grid.nodulo_chegada_selecionado is True:
            grid.partida_e_chegada_definidos = True

        if comecar is True and grid.partida_e_chegada_definidos is True:
            if grid.visualizar_a_star is False:

                grid.visualizar_a_star = True
                resultados_a_star = []
                tempo_gasto = 0

                if a_star_utilizado == 1:

                    t1 = time.perf_counter()
                    resultados_a_star = grid.a_star(grid.nodulo_partida, grid.nodulo_chegada)
                    t2 = time.perf_counter()
                    tempo_gasto = t2 - t1
                    print("versao A* utilizado: V1")

                if a_star_utilizado == 2:
                    t1 = time.perf_counter()
                    resultados_a_star = grid.a_star_v2(grid.nodulo_partida, grid.nodulo_chegada)
                    t2 = time.perf_counter()
                    tempo_gasto = t2 - t1
                    print("versao A* utilizado: V2")

                if resultados_a_star is None:
                    print("nao ha caminho")
                    print("-------------------------------------------")
                else:

                    lista_bruta, lista_refinada = resultados_a_star[0], resultados_a_star[1]
                    print("o tempo total demorado foi de: {} segundos".format(tempo_gasto))
                    print("o caminho contem: ", len(lista_refinada))
                    print("qnt de celulas testadas: ", len(lista_bruta))
                    print("-------------------------------------------")

        # lista bruta: eh a lista que contem a procura do caminho
        # lista refinada: eh a lista que contem o caminho de fato

        grid.update_grid(janela)
        pygame.display.update()


if __name__ == "__main__":
    main()

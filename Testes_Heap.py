from ClasseHeapCelulasGrid import HeapCelulasGrid
from ClasseCelulaV4 import CelulaGridV4
import random

heap = HeapCelulasGrid()

qnt_celulas = int(input("digite o numero de celulas: "))

# teste para ver valores10 sendo adicionados na heap
print("ADCIONADO CELULAS NA HEAP")

for n in range(qnt_celulas):
    x_aleatorio = random.randint(0, 100)
    y_aleatorio = random.randint(0, 100)
    f_aleatorio = random.randint(0, 100)
    nova_celula = CelulaGridV4(x_aleatorio, y_aleatorio, f=f_aleatorio)

    heap.add_celula_heap(nova_celula)
    lista_valores_f = [celula.f for celula in heap.lista_heap_celulas]
    print("a heap agr eh: ", lista_valores_f)

print("--------------------------------------")

# teste para ver valores sendo retirados da heap
print("REMOVENDO CELULAS DA HEAP")

while heap.qnt_celulas_heap > 0:
    lista_valores_f = [celula.f for celula in heap.lista_heap_celulas]
    print("a heap agr eh: ", lista_valores_f)
    heap.remover_primeira_celula_heap()



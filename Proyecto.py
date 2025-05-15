import time
from typing import List

def verificar_tipicidad_fila(fila, matriz, testores, testor_ubi):
    suma = sum(matriz[fila][i] for i in testores[testor_ubi])
    return suma >= 1

def compatibilidad_testores(col, testores, testor_ubi, fila, matriz):
    testores_tip = testores[testor_ubi][:]
    matriz_apoyo = [[matriz[i][indice] for indice in testores[testor_ubi]] + [matriz[i][col]] for i in range(fila + 1)]
    cnt = sum(sum(fila) == 1 for fila in matriz_apoyo)

    if cnt >= len(testores[testor_ubi]):
        matriz_apoyo = [fila for fila in matriz_apoyo if sum(fila) <= 1]
        todos_mayores_o_iguales_a_uno = all(sum(columna) >= 1 for columna in zip(*matriz_apoyo))

        if todos_mayores_o_iguales_a_uno:
            testores_tip.append(col)
        else:
            testores_tip.clear()
    else:
        testores_tip.clear()

    return testores_tip

def completa_testores_tipicos(fila, matriz, testores):
    testores_nuevos = []
    n_columnas = len(matriz[0])

    for i in range(len(testores)):
        if not verificar_tipicidad_fila(fila, matriz, testores, i):
            columnas_a_probar = [j for j in range(n_columnas) if matriz[fila][j] == 1]
            for k in columnas_a_probar:
                testor_apoyo = compatibilidad_testores(k, testores, i, fila, matriz)
                if testor_apoyo:
                    testores_nuevos.append(testor_apoyo)
        else:
            testores_nuevos.append(testores[i])

    testores[:] = testores_nuevos
    
def matriz_testores_tipicos(testores, columnas):
    matriz_b = [[0 for _ in range(columnas)] for _ in range(len(testores))]

    for i in range(len(testores)):
        for j in range(len(testores[i])):
            matriz_b[i][testores[i][j]] = 1

    return matriz_b
  
def theta(matriz_a, matriz_b):
    matriz_theta = []
    for i in range(len(matriz_a)):
        for j in range(len(matriz_b)):
            filas = matriz_a[i] + matriz_b[j]
            matriz_theta.append(filas)
    return matriz_theta

def gamma(matriz_a, matriz_b):
    matriz_gamma = []
    for i in range(len(matriz_a)):
        fila = matriz_a[i] + [0] * len(matriz_b[0])
        matriz_gamma.append(fila)

    for i in range(len(matriz_b)):
        fila = [0] * len(matriz_a[0]) + matriz_b[i]
        matriz_gamma.append(fila)

    return matriz_gamma

def fi(repeticion, matriz_theta):
    if repeticion == 1:
        return matriz_theta
    else:
        matriz_fi = []
        for i in range(len(matriz_theta)):
            filas = []
            for j in range(repeticion):
                filas += matriz_theta[i]
            matriz_fi.append(filas)
        return matriz_fi

def mayores_filas_sort(matriz: List[List[int]]) -> List[List[int]]:
    matriz_a_ordenar = [fila[:] for fila in matriz]

    def contar_unos(fila):
        return fila.count(1)

    def comparador_por_unos(a):
        return contar_unos(a)

    matriz_a_ordenar.sort(key=comparador_por_unos, reverse=True)
    return matriz_a_ordenar


# Programa principal
testores_tipicos = []
matrizA = [
    [1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [0, 1, 0, 1, 1],
    [1, 1, 0, 1, 0]
]

for fila in matrizA:
    print(' '.join(map(str, fila)))

testores_tipicos = [[i] for i, val in enumerate(matrizA[0]) if val == 1]

for i in range(1, len(matrizA)):
    completa_testores_tipicos(i, matrizA, testores_tipicos)

for testor in testores_tipicos:
    print("{ " + ' '.join(f"x{index + 1}" for index in testor) + " }")

################################################################################

MatrizB = matriz_testores_tipicos(testores_tipicos, len(matrizA[0]))

testores_tipicos = []

for fila in MatrizB:
    print(' '.join(map(str, fila)))

testores_tipicos = [[i] for i, val in enumerate(MatrizB[0]) if val == 1]

for i in range(1, len(MatrizB)):
    completa_testores_tipicos(i, MatrizB, testores_tipicos)

for testor in testores_tipicos:
    print("{ " + ' '.join(f"x{index + 1}" for index in testor) + " }")

##########################################################################

Theta = theta(matrizA,MatrizB)

testores_tipicos = []

for fila in Theta:
    print(' '.join(map(str, fila)))

testores_tipicos = [[i] for i, val in enumerate(Theta[0]) if val == 1]

for i in range(1, len(Theta)):
    completa_testores_tipicos(i, Theta, testores_tipicos)

for testor in testores_tipicos:
    print("{ " + ' '.join(f"x{index + 1}" for index in testor) + " }")

################################################################################

Gamma_2 = gamma(Theta,Theta)
Gamma = gamma(Gamma_2,Gamma_2)
testores_tipicos = []

tiempo_inicio = time.time()

for fila in Gamma:
    print(' '.join(map(str, fila)))

testores_tipicos = [[i] for i, val in enumerate(Gamma[0]) if val == 1]

for i in range(1, len(Gamma)):
    completa_testores_tipicos(i, Gamma, testores_tipicos)

#for testor in testores_tipicos:
    #print("{ " + ' '.join(f"x{index + 1}" for index in testor) + " }")

for _ in range(1000000):
    _ = _ * 2

tiempo_fin = time.time()

tiempo_total = tiempo_fin - tiempo_inicio

print(f"El tiempo total de ejecución fue: {tiempo_total} segundos")
print(f"Tiene un total de testores tipicos de: {len(testores_tipicos)}")
print(f"Filas: {len(Gamma)}")
print(f"Columnas: {len(Gamma[0])}")

################################################################################
Fi = fi(5,Theta)

testores_tipicos = []

tiempo_inicio = time.time()

for fila in Fi:
    print(' '.join(map(str, fila)))

testores_tipicos = [[i] for i, val in enumerate(Fi[0]) if val == 1]

for i in range(1, len(Fi)):
    completa_testores_tipicos(i, Fi, testores_tipicos)

#for testor in testores_tipicos:
   # print("{ " + ' '.join(f"x{index + 1}" for index in testor) + " }")

for _ in range(1000000):
    _ = _ * 2

tiempo_fin = time.time()

tiempo_total = tiempo_fin - tiempo_inicio

print(f"El tiempo total de ejecución fue: {tiempo_total} segundos")
print(f"Tiene un total de testores tipicos de: {len(testores_tipicos)}")
print(f"Filas: {len(Fi)}")
print(f"Columnas: {len(Fi[0])}")
################################################################################
Matriz_sort = mayores_filas_sort(Gamma)
testores_tipicos = []

tiempo_inicio = time.time()

for fila in Matriz_sort:
    print(' '.join(map(str, fila)))

testores_tipicos = [[i] for i, val in enumerate(Matriz_sort[0]) if val == 1]

for i in range(1, len(Matriz_sort)):
    completa_testores_tipicos(i, Matriz_sort, testores_tipicos)

#for testor in testores_tipicos:
    #print("{ " + ' '.join(f"x{index + 1}" for index in testor) + " }")

for _ in range(1000000):
    _ = _ * 2

tiempo_fin = time.time()

tiempo_total = tiempo_fin - tiempo_inicio

print(f"El tiempo total de ejecución fue: {tiempo_total} segundos")
print(f"Tiene un total de testores tipicos de: {len(testores_tipicos)}")
print(f"Filas: {len(Matriz_sort)}")
print(f"Columnas: {len(Matriz_sort[0])}")

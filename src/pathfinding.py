import numpy as np
import windData as wd

data_list = wd.get_formatted_dataset()

X = []
Y = []
U = []
V = []

for data in data_list:
    Y.append(data.lat)
    X.append(data.lon)
    U.append(data.u10)
    V.append(data.v10)

field1 = []
x = 0
for data in Y:
    field2 = []
    for data2 in X:
        field2.append([U[x],V[x]])
        x = x + 1
    field1.append(field2)
field = np.array(field1)

field = field / np.sqrt(np.sum(field**2, axis=2, keepdims=True))

def pathField(iniLat, iniLon, goalLat, goalLon):


    iniY = Y.index(iniLat)
    iniX = X.index(iniLon)
    goalY = Y.index(goalLat)
    goalX = X.index(goalLon)

    goal = np.array([iniX, iniY])
    pos = np.array([goalX, goalY])

    # Cria um vetor com as posições do agente
    path = [pos]

    # Enquanto a posição atual do agente for diferente do objetivo
    while not np.array_equal(pos, goal):

        # Calcula a direção do campo vetorial na posição atual
        direction = field[int(pos[0]), int(pos[1])]

        # Move o agente na direção do campo vetorial
        pos = np.clip(pos + direction, 0, len(Y)-1)

        # Adiciona a nova posição à lista de caminho percorrido
        path.append(pos)

    # Converte o caminho percorrido em uma matriz
    path = np.array(path)

    return path


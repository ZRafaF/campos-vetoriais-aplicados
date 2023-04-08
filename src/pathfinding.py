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

Y = list(dict.fromkeys(Y))
X = list(dict.fromkeys(X))
U10 = np.array(U)
V10 = np.array(V)

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

        uniU = U10[int(pos[0]*len(Y)) + int(pos[1])]
        uniV = V10[int(pos[0]*len(Y)) + int(pos[1])]
        uniU = uniU / np.sqrt(uniU**2 + uniV**2)
        uniV = uniV / np.sqrt(uniU**2 + uniV**2)
        # Calcula a direção do campo vetorial na posição atual
        direction = [uniU, uniV]

        # Move o agente na direção do campo vetorial
        pos = np.clip(pos + direction, 0, len(Y)-1)

        # Adiciona a nova posição à lista de caminho percorrido
        path.append(pos)

    # Converte o caminho percorrido em uma matriz
    path = np.array(path)

    return path


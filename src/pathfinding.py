import numpy as np
import windData as wd



def pathField(iniLat, iniLon, goalLat, goalLon):
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

    iniY = Y.index(iniLat)
    iniX = X.index(iniLon)
    goalY = Y.index(goalLat)
    goalX = X.index(goalLon)

    goal = np.array([goalX, goalY])
    ini = np.array([iniX, iniY])
    pos = np.array([iniX, iniY])

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
        
        ant = [abs(goal[0] - pos[0]), abs(goal[1] - pos[1])]
        # Move o agente na direção do campo vetorial
        pos = np.clip(pos + direction, ini, goal)

        if((ant[0] <= abs(goal[0] - pos[0])) and pos[0] != goal[0]):
            if(goal[0] > pos[0]):
                if(pos[0] + 1 < goal[0]):
                    pos[0] = pos[0] + 1
                else:
                    pos[0] = goal[0]
            else:
                if(pos[0] - 1 > goal[0]):
                    pos[0] = pos[0] - 1
                else:
                    pos[0] = goal[0]
        if((ant[1] <= abs(goal[1] - pos[1])) and pos[1] != goal[1]):
            if(goal[1] > pos[1]):
                if(pos[1] + 1 < goal[1]):
                    pos[1] = pos[1] + 1
                else:
                    pos[1] = goal[1]
            else:
                if(pos[1] - 1 > goal[1]):
                    pos[1] = pos[1] - 1
                else:
                    pos[1] = goal[1]
        # Adiciona a nova posição à lista de caminho percorrido
        path.append(pos)

    # Converte o caminho percorrido em uma matriz

    pathLatLon = []
    for cord in path:
        pathLatLon.append([X[int(cord[0])], Y[int(cord[1])]])

    path = np.array(pathLatLon)
    
    return path

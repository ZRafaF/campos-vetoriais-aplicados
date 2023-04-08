import numpy as np
import matplotlib.pyplot as plt
import windData as wd

dataset = wd.get_formatted_dataset()
X = []
Y = []
U = []
V = []

for data in dataset:
    Y.append(data.lat)
    X.append(data.lon)
    U.append(data.u10)
    V.append(data.v10)


#latitude = y
#longitude = x
#u horizontal
#v vertical


x,y = np.meshgrid( np.linspace( -75, -32, 10), np.linspace( -35, 6, 10))

plt.quiver(X,Y,U,V)
plt.grid('on')
plt.show()

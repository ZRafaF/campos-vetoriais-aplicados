import numpy as np
import matplotlib.pyplot as plt

#latitude = y
#longitude = x
#u horizontal
#v vertical


x,y = np.meshgrid( np.linspace( -100, 100, 25), np.linspace( -100, 100, 25))
u = y - 1
v = x/4

plt.quiver(x,y,u,v)
plt.grid('on')
plt.show()
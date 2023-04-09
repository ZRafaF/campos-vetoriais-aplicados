import numpy as np
import matplotlib.pyplot as plt
import windData as wd
from typing import List


def plot_vector_field(vector_field: List[wd.FormattedData]):
    """Recebe um vector field no formato List[wd.FormattedData] e o plota"""
    X = []
    Y = []
    U = []
    V = []

    for data in vector_field:
        Y.append(data.lat)
        X.append(data.lon)
        U.append(data.u10)
        V.append(data.v10)

    # latitude = y
    # longitude = x
    # u horizontal
    # v vertical

    x, y = np.meshgrid(np.linspace(-75, -32, 10), np.linspace(-35, 6, 10))

    plt.quiver(X, Y, U, V)
    plt.grid("on")
    plt.show()


def plot_vector_field_and_path(
    vector_field: List[wd.FormattedData], path: List[np.array]
):
    """Recebe um vector field no formato List[wd.FormattedData] e o plota"""
    X = []
    Y = []
    U = []
    V = []

    for data in vector_field:
        Y.append(data.lat)
        X.append(data.lon)
        U.append(data.u10)
        V.append(data.v10)

    # latitude = y
    # longitude = x
    # u horizontal
    # v vertical

    x, y = np.meshgrid(np.linspace(-75, -32, 10), np.linspace(-35, 6, 10))

    plt.quiver(X, Y, U, V)
    plt.grid("on")
    plt.plot(path, color="r")

    plt.show()

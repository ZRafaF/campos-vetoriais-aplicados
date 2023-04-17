import matplotlib.pyplot as plt
import windData as wd
from typing import List, Tuple
from typing import List, Tuple


def plot_vector_field(vector_field: List[wd.FormattedData]):
    """Recebe um vector field no formato List[wd.FormattedData] e o plota"""
    X = []
    Y = []
    U = []
    V = []

    for data in vector_field:
        Y.append(data.lat)
        X.append(data.lon)
        U.append(data.u100)
        V.append(data.v100)

    # latitude = y
    # longitude = x
    # u horizontal
    # v vertical

    # Essa linha não tava fazendo nada
    # x, y = np.meshgrid(np.linspace(-75, -32, 10), np.linspace(-35, 6, 10))

    plt.quiver(X, Y, U, V)
    plt.grid("on")


def plot_path(path: List[Tuple[float, float]], color: str = "r"):
    """Recebe um caminho e o plota"""
    last_point = None
    for point in path:
        if last_point is not None:
            plt.plot([point[0], last_point[0]], [point[1], last_point[1]], color=color)
        last_point = point


def plot_point(point: Tuple[float, float], color: str = "r"):
    plt.plot(point[0], point[1], color=color, marker="o", markersize=3)


def show_plot():
    plt.show()

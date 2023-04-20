import matplotlib.pyplot as plt
import windData as wd
from typing import List, Tuple
from typing import List, Tuple
import numpy as np
from scipy.interpolate import UnivariateSpline
import networkx as nx


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
            plt.plot([point[1], last_point[1]], [point[0], last_point[0]], color=color)
        last_point = point


def plot_path_smooth(path: List[Tuple[float, float]], color: str = "r"):
    """Recebe um caminho, interpola e o plota"""
    SMOOTH = 0.4
    points = np.array(path)

    distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    distance = np.insert(distance, 0, 0) / distance[-1]

    splines = [UnivariateSpline(distance, coords, k=3, s=SMOOTH) for coords in points.T]

    alpha = np.linspace(0, 1, 100)
    points_fitted = np.vstack(spl(alpha) for spl in splines).T

    plt.plot(*points_fitted.T, color=color)


def plot_point(point: Tuple[float, float], color: str = "r"):
    plt.plot(point[1], point[0], color=color, marker="o", markersize=3)


def show_plot():
    plt.show()


def plot_heatmap(matrix):
    plt.figure(2)

    plt.imshow(matrix, cmap="hot", interpolation="nearest")


def draw_graph(G):
    weights_raw = list(nx.get_edge_attributes(G, "weight").values())
    weights = [(x - wd.WIND_OFFSET) / 10 for x in weights_raw]

    nx.draw(
        G,
        pos=nx.spring_layout(G),
        with_labels=False,
        node_size=2,
        width=list(weights),
    )
    plt.show()


def draw_weighted_matrix(start, goal):
    weighted_matrix, start_idx, goal_idx = wd.make_weighted_matrix(start, goal)
    plot_heatmap(weighted_matrix)

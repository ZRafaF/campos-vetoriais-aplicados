import matplotlib.pyplot as plt
import windData as wd
from typing import List, Tuple
import numpy as np
from scipy.interpolate import UnivariateSpline
import networkx as nx


def plot_vector_field(vector_field: List[wd.FormattedData]):
    """Receives a vector field in the format List[wd.FormattedData] and plots it"""
    X = []
    Y = []
    U = []
    V = []

    for data in vector_field:
        Y.append(data.lat)
        X.append(data.lon)
        U.append(data.u100)
        V.append(data.v100)

    # Create a quiver plot of the vector field
    plt.quiver(X, Y, U, V)
    plt.grid("on")


def plot_path(path: List[Tuple[float, float]], color: str = "r"):
    """Receives a path and plots it"""
    last_point = None
    for point in path:
        if last_point is not None:
            plt.plot([point[1], last_point[1]], [point[0], last_point[0]], color=color)
        last_point = point


def km_to_degrees(distance_km):
    """
    Converts a distance in kilometers to an angular measurement in degrees on the surface of the Earth.

    Args:
    distance_km (float): The distance in kilometers.

    Returns:
    The angular measurement in degrees.
    """
    circumference_km = 40075  # Circumference of the Earth at the equator in kilometers
    circumference_degrees = 360  # Circumference of the Earth in degrees
    degrees_per_km = circumference_degrees / circumference_km
    degrees = distance_km * degrees_per_km
    return degrees


def plot_radius(start: Tuple[float, float], radius: float, color: str = "r"):
    """
    Receives a start point, a radius in kilometers, and a color, and plots a circle of the specified radius around the start point.

    Args:
    start (Tuple[float, float]): The coordinates of the start point.
    radius (float): The radius of the circle in kilometers.
    color (str, optional): The color of the circle. Defaults to "r".
    """
    # Convert the radius from kilometers to degrees of latitude
    lat_radius = km_to_degrees(radius)
    # Plot the circle
    circle = plt.Circle((start[1], start[0]), lat_radius, color=color, fill=False)
    _, ax = plt.subplots()
    ax.add_patch(circle)


def plot_path_smooth(path: List[Tuple[float, float]], color: str = "r"):
    """Recebe um caminho, interpola e o plota"""
    # Constant used to adjust smoothness of the path interpolation
    SMOOTH = 0.4
    # Convert the path to a NumPy array for easier calculations
    points = np.array(path)

    # Calculate the cumulative distance between the points in the path
    distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    distance = np.insert(distance, 0, 0) / distance[-1]

    # Use the distance and coordinates to create a spline for each dimension of the path
    splines = [UnivariateSpline(distance, coords, k=3, s=SMOOTH) for coords in points.T]

    # Use the splines to create a smooth path with 100 points
    alpha = np.linspace(0, 1, 100)
    points_fitted = np.vstack([spl(alpha) for spl in splines]).T

    # Plot the smooth path using Matplotlib
    plt.plot(*points_fitted.T, color=color)

    # Plot the start and goal points of the path
    plot_point((path[0][1], path[0][0]), "b")
    plot_point((path[len(path) - 1][1], path[len(path) - 1][0]), "g")


def plot_point(point: Tuple[float, float], color: str = "r"):
    """Plot a point using Matplotlib"""
    plt.plot(point[1], point[0], color=color, marker="o", markersize=3)


def show_plot():
    """Show the plot using Matplotlib"""
    plt.show()


def plot_heatmap(matrix):
    """Plot a heatmap using Matplotlib"""
    plt.imshow(matrix, cmap="viridis", interpolation="nearest")


def draw_graph(G):
    """Draw a graph using NetworkX and Matplotlib"""
    # Get the weights of the edges in the graph and adjust them for plotting
    weights_raw = list(nx.get_edge_attributes(G, "weight").values())
    weights = [(x - wd.WIND_OFFSET) / 10 for x in weights_raw]

    # Draw the graph using NetworkX and Matplotlib
    nx.draw(
        G,
        pos=nx.spring_layout(G),
        with_labels=False,
        node_size=2,
        width=list(weights),
    )

    plt.show()

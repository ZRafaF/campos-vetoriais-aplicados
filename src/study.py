# Copyright (c) 2023 A Comunidade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import networkx as nx
import windData as wd
from typing import Tuple
import pandas as pd
import math
from tqdm import tqdm


def get_G(graph: pd.DataFrame) -> any:
    return nx.from_pandas_edgelist(
        graph, source="source", target="target", edge_attr="weight"
    )


def get_shortest_path(
    G: any,
    start: Tuple[float, float],
    goal: Tuple[float, float],
    method: str = "dijkstra",
) -> list:
    """
    Para mais info https://networkx.guide/algorithms/shortest-path/
    """

    start_lat_idx, start_lon_idx = wd.get_nearest_point_index(start[0], start[1])
    goal_lat_idx, goal_lon_idx = wd.get_nearest_point_index(goal[0], goal[1])
    return nx.shortest_path(
        G,
        source=wd.get_1d_from_2d(start_lat_idx, start_lon_idx),
        target=wd.get_1d_from_2d(goal_lat_idx, goal_lon_idx),
        weight="weight",
        method=method,
    )


def get_shortest_path_astar(
    G: any,
    start: Tuple[float, float],
    goal: Tuple[float, float],
) -> list:
    """
    Utiliza o algoritmo A* para encontrar o caminho mais próximo
    """
    start_lat_idx, start_lon_idx = wd.get_nearest_point_index(start[0], start[1])
    goal_lat_idx, goal_lon_idx = wd.get_nearest_point_index(goal[0], goal[1])
    return nx.astar_path(
        G,
        source=wd.get_1d_from_2d(start_lat_idx, start_lon_idx),
        target=wd.get_1d_from_2d(goal_lat_idx, goal_lon_idx),
        weight="weight",
    )


def get_lat_lon_from_1d(idx_1d):
    """
    Convert a 1D index to a tuple of (longitude, latitude) coordinates.

    Args:
        idx_1d (int): 1D index of a point in the grid.

    Returns:
        tuple: A tuple of (longitude, latitude) coordinates.
    """
    point = wd.get_2d_from_1d(idx_1d)
    lat = wd.get_latitude_list()[point[1]]
    lon = wd.get_longitude_list()[point[0]]
    return (lon, lat)


def get_path_2d_from_1d(path: list) -> list:
    """
    Convert a list of 1D indices representing a path to a list of (longitude, latitude) coordinates.

    Args:
        path (list): A list of 1D indices representing a path.

    Returns:
        list: A list of (longitude, latitude) coordinates representing the same path.
    """
    return list(map(lambda x: get_lat_lon_from_1d(x), path))


def get_path_2d_cost(path_2d: list) -> float:
    """
    Calculate the total cost of a path in km.

    Args:
        path_2d (list): A list of (longitude, latitude) coordinates representing a path.

    Returns:
        float: The total cost of the path in km.
    """
    last_point = None
    total_cost: float = 0
    for point in path_2d:
        if last_point is not None:
            # Calculate the cost between the current point and the previous point
            cost = wd.calculate_cost_between_points(
                last_point[1], last_point[0], point[1], point[0]
            )
            total_cost += cost
        last_point = point
    return total_cost


def get_shortest_path_in_radius(start: tuple, radius: float, G: any) -> list:
    """
    This function returns the shortest path between the start location and a point within a certain radius.
    The radius is in kilometers.
    """
    # Initialize an empty list to store all paths and their costs.
    all_paths_2d_cost = []

    # Initialize a progress bar to track the loop progress.
    print("Procurando o melhor caminho no raio...")
    progress_bar = tqdm(range(36))

    # Loop through 36 angles (10 degrees each).
    for angle in range(36):
        progress_bar.update(1)  # Update the progress bar.

        # Calculate the latitude and longitude of the goal point given the start location, radius, and angle.
        goal = get_new_latitude_longitude(start[0], start[1], radius, angle * 10)

        # Find the index of the nearest point on the graph to the goal point.
        nearest_lat, nearest_lon = wd.get_nearest_point_index(goal[0], goal[1])

        # If the nearest point cannot be found, skip this iteration.
        if nearest_lat == -1 or nearest_lon == -1:
            continue

        try:
            # Calculate the shortest path between the start point and the goal point.
            path = get_shortest_path(G, start, goal)

            # Convert the path to a 2D representation.
            path_2d = get_path_2d_from_1d(path)

            # Calculate the cost of the 2D path.
            cost = get_path_2d_cost(path_2d)

            # Add the path and its cost to the list.
            all_paths_2d_cost.append({"path": path, "cost": cost})
        except:
            pass
    # Find the path with the lowest cost.
    lowest_cost = math.inf
    lowest_cost_idx = 0
    for idx, path_2d_cost in enumerate(all_paths_2d_cost):
        if path_2d_cost["cost"] < lowest_cost:
            lowest_cost = path_2d_cost["cost"]
            lowest_cost_idx = idx
    progress_bar.close()  # Close the progress bar.

    # Return the path with the lowest cost.
    return all_paths_2d_cost[lowest_cost_idx]["path"]


def get_new_latitude_longitude(
    lat: float, lon: float, radius_in_km: float, angle_in_degrees: float
) -> Tuple[float, float]:
    """
    Returns new latitude and longitude coordinates based on the given parameters.

    Args:
    lat (float): The latitude coordinate in degrees.
    lon (float): The longitude coordinate in degrees.
    radius_in_km (float): The radius in kilometers.
    angle_in_degrees (float): The angle in degrees.

    Returns:
    A tuple containing the new latitude and longitude coordinates.
    """
    # Convert latitude, longitude, and angle to radians
    lat_radians = math.radians(lat)
    lon_radians = math.radians(lon)
    angle_radians = math.radians(angle_in_degrees)

    # Calculate the new latitude and longitude using the Haversine formula
    earth_radius = 6371  # in kilometers
    new_lat = math.asin(
        math.sin(lat_radians) * math.cos(radius_in_km / earth_radius)
        + math.cos(lat_radians)
        * math.sin(radius_in_km / earth_radius)
        * math.cos(angle_radians)
    )
    new_lon = lon_radians + math.atan2(
        math.sin(angle_radians)
        * math.sin(radius_in_km / earth_radius)
        * math.cos(lat_radians),
        math.cos(radius_in_km / earth_radius)
        - math.sin(lat_radians) * math.sin(new_lat),
    )

    # Convert the new latitude and longitude back to degrees
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    # Return the new latitude and longitude as a tuple
    return (new_lat, new_lon)

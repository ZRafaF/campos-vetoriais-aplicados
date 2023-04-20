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
    point = wd.get_2d_from_1d(idx_1d)
    lat = wd.get_latitude_list()[point[1]]
    lon = wd.get_longitude_list()[point[0]]
    return (lon, lat)


def get_path_2d_from_1d(path: list) -> list:
    return list(map(lambda x: get_lat_lon_from_1d(x), path))


def get_path_2d_cost(path_2d: list) -> float:
    last_point = None
    total_cost: float = 0
    for point in path_2d:
        if last_point is not None:
            cost = wd.calculate_cost_between_points(
                last_point[1], last_point[0], point[1], point[0]
            )
            total_cost += cost
        last_point = point
    return total_cost


def get_shortest_path_in_radius(start: tuple, radius: float, G: any) -> list:
    "Radius in km"
    all_paths_2d_cost = []
    progress_bar = tqdm(range(36))

    for angle in range(36):
        goal = get_new_latitude_longitude(start[0], start[1], radius, angle * 10)
        path = get_shortest_path(G, start, goal)
        path_2d = get_path_2d_from_1d(path)
        cost = get_path_2d_cost(path_2d)
        all_paths_2d_cost.append({"path": path, "cost": cost})
        progress_bar.update(1)

    lowest_cost = math.inf
    lowest_cost_idx = 0
    for idx, path_2d_cost in enumerate(all_paths_2d_cost):
        if path_2d_cost["cost"] < lowest_cost:
            lowest_cost = path_2d_cost["cost"]
            lowest_cost_idx = idx
    progress_bar.close()

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

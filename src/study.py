# Copyright (c) 2023 A Comunidade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import networkx as nx
import windData as wd
from typing import Tuple
import pandas as pd


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

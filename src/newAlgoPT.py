# Copyright (c) 2023 A Comunidade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from typing import List, Tuple
import windData as wd
import math
from tqdm import tqdm
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder


def bellman_ford(graph, start, end):
    """
    Find the shortest path between start and end nodes in a weighted 2D array using the Bellman-Ford algorithm.

    Args:
        graph (List[List[int]]): The weighted 2D array representing the graph.
        start (Tuple[int, int]): The starting point.
        end (Tuple[int, int]): The ending point.

    Returns:
        List[Tuple[int, int]]: The shortest path from start to end nodes.
    """
    rows, cols = len(graph), len(graph[0])
    distances = {(i, j): float("inf") for i in range(rows) for j in range(cols)}
    distances[start] = 0
    parents = {}

    for _ in range(rows * cols - 1):
        for i in range(rows):
            print(i)
            for j in range(cols):
                for neighbor in get_neighbors((i, j), rows, cols):
                    cost = graph[neighbor[0]][neighbor[1]]
                    if distances[(i, j)] + cost < distances[neighbor]:
                        distances[neighbor] = distances[(i, j)] + cost
                        parents[neighbor] = (i, j)

    for i in range(rows):
        print(i)
        for j in range(cols):
            for neighbor in get_neighbors((i, j), rows, cols):
                cost = graph[neighbor[0]][neighbor[1]]
                if distances[(i, j)] + cost < distances[neighbor]:
                    # Negative weight cycle detected
                    return None

    path = []
    node = end
    while node != start:
        path.append(node)
        node = parents[node]
    path.append(start)
    return list(reversed(path))


def get_neighbors(node, rows, cols):
    """
    Get the neighbors of a node in a 2D grid.

    Args:
        node (Tuple[int, int]): The node.
        rows (int): The number of rows in the 2D grid.
        cols (int): The number of columns in the 2D grid.

    Returns:
        List[Tuple[int, int]]: The neighbors of the node.
    """
    (x, y) = node
    neighbors = []

    if x > 0:
        neighbors.append((x - 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if x < rows - 1:
        neighbors.append((x + 1, y))
    if y < cols - 1:
        neighbors.append((x, y + 1))

    return neighbors


def find_angle(x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    if angle < 0:
        angle += 360
    return angle


def calculate_cost(angle: float, u: float, v: float):
    angle += 90
    # Calculate the angle of the vector relative to the x-axis
    vector_angle = math.atan2(v, u) * 180 / math.pi

    # Calculate the angle between the vector and the line
    angle_diff = angle - vector_angle

    # Calculate the projection of the vector onto the line
    projection = math.cos(angle_diff * math.pi / 180) * math.sqrt(u**2 + v**2)

    return round(projection * 100, 0)


def find_path(
    start: Tuple[float, float],
    goal: Tuple[float, float],
    vector_field: List[wd.FormattedData],
):
    angle = find_angle(start[0], start[1], goal[0], goal[1])
    print("angle: ", angle)
    matrix = []
    progress_bar = tqdm(wd.get_latitude_list())
    for idx_lat in range(len(wd.get_latitude_list())):
        new_row = []
        for idx_lon in range(len(wd.get_longitude_list())):
            wind_at_point = wd.get_wind_by_idx(idx_lat, idx_lon, "100")
            new_row.append(calculate_cost(angle, wind_at_point[0], wind_at_point[1]))
        matrix.append(new_row)
        progress_bar.update(1)
    progress_bar.close()

    start_tuple_idx = wd.get_nearest_point_index(start[0], start[1])
    end_tuple_idx = wd.get_nearest_point_index(goal[0], goal[1])

    grid = Grid(matrix=matrix)
    start = grid.node(start_tuple_idx[0], start_tuple_idx[1])
    end = grid.node(end_tuple_idx[0], end_tuple_idx[1])

    finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always, time_limit=30)
    path, runs = finder.find_path(start, end, grid)
    print("operations:", runs, "path length:", len(path))
    print(grid.grid_str(path=path, start=start, end=end))

    return 0

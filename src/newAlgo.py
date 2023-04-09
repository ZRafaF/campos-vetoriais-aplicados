# Copyright (c) 2023 A Comunidade
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
from typing import List, Tuple
import windData as wd
import math


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

    return round(projection, 5)


def find_path(
    start: Tuple[float, float],
    goal: Tuple[float, float],
    vector_field: List[wd.FormattedData],
):
    angle = find_angle(start[0], start[1], goal[0], goal[1])
    print("angle: ", angle)

    grid = []
    for lat in wd.get_latitude_list():
        new_row = []
        for lon in wd.get_longitude_list():
            wind_at_point = wd.get_wind_at(lat, lon, "100")
            new_row.append(calculate_cost(angle, wind_at_point[0], wind_at_point[1]))
        grid.append(new_row)
    print(grid)
    return 0

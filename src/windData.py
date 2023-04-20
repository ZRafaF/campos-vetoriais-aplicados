# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import netCDF4 as nc
from typing import List, Tuple, Dict
from tqdm import tqdm
import math
import pandas as pd
import os.path


class FormattedData:
    def __init__(
        self,
        lat: float,
        lon: float,
        u10: float = 0,
        v10: float = 0,
        u10n: float = 0,
        v10n: float = 0,
        u100: float = 0,
        v100: float = 0,
    ):
        self.lat = lat
        self.lon = lon

        # Componente do vento horizontal em m/s
        self.u10 = u10  # Componente a 10m
        self.u10n = u10n  # Componente do vento neutro a 10m
        self.u100 = u100  # Componente a 100m

        # Componente do vento vertical em m/s
        self.v10 = v10  # Componente a 10m
        self.v10n = v10n  # Componente do vento neutro a 10m
        self.v100 = v100  # Componente a 100m


def load_data_set() -> List[float]:
    """Carrega o dataset de um arquivo"""
    return nc.Dataset(DATASET_PATH)


def get_variables() -> List[float]:
    """Retorna as variáveis presentes no dataset"""
    return dataset.variables


def get_keys():
    """Retorna os tipos de dados disponíveis no dataset"""
    return dataset.variables.keys()


def get_latitude_list() -> List[float]:
    """Retorna um iterador das latitudes"""
    return dataset.variables["latitude"][:]


def get_longitude_list() -> List[float]:
    """Retorna um iterador das longitudes"""
    return dataset.variables["longitude"][:]


def get_v10_list() -> List[float]:
    """Retorna um iterador da velocidade do vento no componente v10 'latitudinal'"""
    return dataset.variables["v10"][0]


def get_u10_list() -> List[float]:
    """Retorna um iterador da velocidade do vento no componente u10 'longitudinal'"""
    return dataset.variables["u10"][0]


def get_v10n_list() -> List[float]:
    """Retorna um iterador da velocidade do vento no componente v10n 'latitudinal'"""
    return dataset.variables["v10n"][0]


def get_u10n_list() -> List[float]:
    """Retorna um iterador da velocidade do vento no componente u10n 'longitudinal'"""
    return dataset.variables["u10n"][0]


def get_v100_list() -> List[float]:
    """Retorna um iterador da velocidade do vento no componente v100 'latitudinal'"""
    return dataset.variables["v100"][0]


def get_u100_list() -> List[float]:
    """Retorna um iterador da velocidade do vento no componente u100 'longitudinal'"""
    return dataset.variables["u100"][0]


def get_formatted_dataset() -> List[FormattedData]:
    """Retorna uma lista de objetos do tipo FormattedData"""

    print("Formatando o dataset...")

    has_wind_10 = True if "u10" in get_keys() else False
    has_wind_10n = True if "u10n" in get_keys() else False
    has_wind_100 = True if "u100" in get_keys() else False

    u10_list = get_u10_list() if has_wind_10 else None
    v10_list = get_v10_list() if has_wind_10 else None

    u10n_list = get_u10n_list() if has_wind_10n else None
    v10n_list = get_v10n_list() if has_wind_10n else None

    u100_list = get_u100_list() if has_wind_100 else None
    v100_list = get_v100_list() if has_wind_100 else None

    formatted_list: List[FormattedData] = []

    progress_bar = tqdm(get_latitude_list())

    for idx_lat, lat in enumerate(get_latitude_list()):
        for idx_lon, lon in enumerate(get_longitude_list()):
            u10 = u10_list[idx_lat][idx_lon] if has_wind_10 else None
            v10 = v10_list[idx_lat][idx_lon] if has_wind_10 else None

            u10n = u10n_list[idx_lat][idx_lon] if has_wind_10n else None
            v10n = v10n_list[idx_lat][idx_lon] if has_wind_10n else None

            u100 = u100_list[idx_lat][idx_lon] if has_wind_100 else None
            v100 = v100_list[idx_lat][idx_lon] if has_wind_100 else None

            formatted_data = FormattedData(lat, lon, u10, v10, u10n, v10n, u100, v100)
            formatted_list.append(formatted_data)
        progress_bar.update(1)
    progress_bar.close()
    return formatted_list


def print_dataset(formatted_dataset: List[FormattedData]) -> None:
    """Recebe uma lista de dados formatados 'List[FormattedData]' e os imprime na tela"""
    for i in formatted_dataset:
        print("lat: ", i.lat, " lon: ", i.lon, " u10: ", i.u10, " v10: ", i.v10)


def __round_num(num: float) -> float:
    """Retorna o numero mais próximo a cada 0.25"""
    remaining = num % 0.25
    return num - remaining


def __get_data_range() -> Dict[int, int]:
    """Retorna um dicionário com os limites do dataset"""
    return {
        "lat": (
            get_latitude_list()[0],
            get_latitude_list()[len(get_latitude_list()) - 1],
        ),
        "lon": (
            get_longitude_list()[0],
            get_longitude_list()[len(get_longitude_list()) - 1],
        ),
    }


def find_angle(x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    if angle < 0:
        angle += 360
    return angle


def get_nearest_point_index(lat: float, lon: float) -> Tuple[float, float]:
    """
    Retorna uma Tuple dos índices dos pontos mais próximos

    Retorna (-1,-1) caso a posição fornecida seja inválida
    """
    lat_idx = -1
    lon_idx = -1

    if lat > DATA_RANGE["lat"][0] or lat < DATA_RANGE["lat"][1]:
        return (lat_idx, lon_idx)
    if lon < DATA_RANGE["lon"][0] or lon > DATA_RANGE["lon"][1]:
        return (lat_idx, lon_idx)

    closest_lat = __round_num(lat)
    closest_lon = __round_num(lon)

    # Checando latitude
    for idx, lat in enumerate(get_latitude_list()):
        if get_latitude_list()[idx] == closest_lat:
            lat_idx = idx
            break

    # Checando longitude
    for idx, lon in enumerate(get_longitude_list()):
        if get_longitude_list()[idx] == closest_lon:
            lon_idx = idx
            break

    return (lat_idx, lon_idx)


def get_wind_by_idx(
    idx_lat: int, idx_lon: int, height: str = "10"
) -> Tuple[float, float]:
    if height == "100":
        return (get_u100_list()[idx_lat][idx_lon], get_v100_list()[idx_lat][idx_lon])
    if height == "10":
        return (get_u10_list()[idx_lat][idx_lon], get_v10_list()[idx_lat][idx_lon])

    if height == "10n":
        return (get_u10n_list()[idx_lat][idx_lon], get_v10n_list()[idx_lat][idx_lon])

    raise ValueError("Altitude inválida")


def get_wind_at(lat: float, lon: float, height: str = "10") -> Tuple[float, float]:
    """
    Retorna os valores de vento de uma determinada posição e altitude.
    As altitudes permitidas são '10', '10n', '100'

    Irá levantar uma exceção caso a posição seja invalida
    """
    idx_lat, idx_lon = get_nearest_point_index(lat, lon)
    if idx_lat == -1 or idx_lon == -1:
        raise ValueError(
            "Posição lat: ",
            lat,
            " lon: ",
            lon,
            " está fora dos limites de dados",
            DATA_RANGE,
        )
    if height == "10":
        return (get_u10_list()[idx_lat][idx_lon], get_v10_list()[idx_lat][idx_lon])

    if height == "10n":
        return (get_u10n_list()[idx_lat][idx_lon], get_v10n_list()[idx_lat][idx_lon])

    if height == "100":
        return (get_u100_list()[idx_lat][idx_lon], get_v100_list()[idx_lat][idx_lon])

    raise ValueError("Altitude inválida")


def calculate_cost(angle: float, u: float, v: float):
    angle += 90
    # Calculate the angle of the vector relative to the x-axis
    vector_angle = math.atan2(v, u) * 180 / math.pi

    # Calculate the angle between the vector and the line
    angle_diff = angle - vector_angle

    # Calculate the projection of the vector onto the line
    projection = math.cos(angle_diff * math.pi / 180) * math.sqrt(u**2 + v**2)

    return projection


def make_weighted_matrix(
    start: Tuple[float, float], goal: Tuple[float, float], height: str = "10"
) -> Tuple[List[List[float]], Tuple[int, int], Tuple[int, int]]:
    """
    Recebe um ponto inicial e final.

    Retorna:
        - Matriz de pesos
        - Tuple com o índice do ponto inicial
        - Tuple com o índice do ponto final
    """
    print("Criando matriz de pesos...")

    angle = find_angle(start[0], start[1], goal[0], goal[1])
    matrix = []
    progress_bar = tqdm(get_latitude_list())

    start_tuple_idx = (0, 0)
    end_tuple_idx = (0, 0)
    for idx_lat, lat in enumerate(get_latitude_list()):
        new_row = []
        for idx_lon, lon in enumerate(get_longitude_list()):
            wind_at_point = get_wind_by_idx(idx_lat, idx_lon, height)
            new_row.append(calculate_cost(angle, wind_at_point[0], wind_at_point[1]))
            if lat == start[0] and lon == start[1]:
                start_tuple_idx = (len(new_row), len(matrix))
            elif lat == goal[0] and lon == goal[1]:
                end_tuple_idx = (len(new_row), len(matrix))
        matrix.append(new_row)
        progress_bar.update(1)
    progress_bar.close()
    return (matrix, start_tuple_idx, end_tuple_idx)


def get_1d_from_2d(x: int, y: int) -> int:
    return y * len(get_latitude_list()) + x


def get_2d_from_1d(idx: int) -> Tuple[int, int]:
    lat_size = len(get_latitude_list())
    return (idx // lat_size, idx % lat_size)


def calculate_cost_positive(angle: float, u: float, v: float):
    angle += 90
    # Calculate the angle of the vector relative to the x-axis
    vector_angle = math.atan2(v, u) * 180 / math.pi

    # Calculate the angle between the vector and the line
    angle_diff = angle - vector_angle

    # Calculate the projection of the vector onto the line
    projection = math.cos(angle_diff * math.pi / 180) * math.sqrt(u**2 + v**2)

    return abs(projection + 9999)


def calculate_cost_between_points(
    start_lat: int, start_lon: int, goal_lat: int, goal_lon: int
) -> float:
    goal_u, goal_v = get_wind_at(goal_lat, goal_lon)
    angle = find_angle(start_lat, start_lon, goal_lat, goal_lon)
    return calculate_cost_positive(angle, goal_u, goal_v)


def make_data_frame() -> pd.DataFrame:
    """ """
    g_source = []
    g_target = []
    g_weight = []

    lat_list = get_latitude_list()
    lon_list = get_longitude_list()

    num_of_row = len(lat_list)
    num_of_col = len(lon_list)

    progress_bar = tqdm(get_latitude_list())

    for lat_idx, lat in enumerate(lat_list):
        for lon_idx, lon in enumerate(lon_list):
            idx_1d = get_1d_from_2d(lon_idx, lat_idx)
            # Get top neighbor
            if lat_idx > 0:
                other_lat_idx = lat_idx - 1
                other_lon_idx = lon_idx

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get down neighbor
            if lat_idx < num_of_row - 1:
                other_lat_idx = lat_idx + 1
                other_lon_idx = lon_idx

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get left neighbor
            if lon_idx > 0:
                other_lat_idx = lat_idx
                other_lon_idx = lon_idx - 1

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get right neighbor
            if lon_idx < num_of_col - 1:
                other_lat_idx = lat_idx
                other_lon_idx = lon_idx + 1

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get top-left neighbor
            if lat_idx > 0 and lon_idx > 0:
                other_lat_idx = lat_idx - 1
                other_lon_idx = lon_idx - 1

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get down-left neighbor
            if lat_idx < num_of_row - 1 and lon_idx > 0:
                other_lat_idx = lat_idx + 1
                other_lon_idx = lon_idx - 1

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get top-right neighbor
            if lat_idx > 0 and lon_idx < num_of_col - 1:
                other_lat_idx = lat_idx - 1
                other_lon_idx = lon_idx + 1

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )

            # Get down-right neighbor
            if lat_idx < num_of_row - 1 and lon_idx < num_of_col - 1:
                other_lat_idx = lat_idx + 1
                other_lon_idx = lon_idx + 1

                g_source.append(idx_1d)

                g_target.append(get_1d_from_2d(other_lon_idx, other_lat_idx))

                g_weight.append(
                    calculate_cost_between_points(
                        lat, lon, lat_list[other_lat_idx], lon_list[other_lon_idx]
                    )
                )
        progress_bar.update(1)
    progress_bar.close()

    data_frame = pd.DataFrame(
        {"source": g_source, "target": g_target, "weight": g_weight}
    )
    data_frame.to_pickle(DATA_FRAME_PATH)

    return data_frame


def load_data_frame() -> pd.DataFrame:
    if os.path.isfile(DATA_FRAME_PATH):
        return pd.read_pickle(DATA_FRAME_PATH)
    print("Data frame não encontrado, criando um novo...")

    response = input(
        "Essa ação pode demorar bastante, pressione 's' para continuar, ou qualquer outra tecla para sair \n"
    )

    if response != "s":
        print("Encerrando...")
        quit()
    return make_data_frame()


DATASET_PATH = "data/data.nc"
"""
    Caminho para o dataset

    Disponíveis na pasta /data/...
"""

DATA_FRAME_PATH = "data/dataframe_data.pkl"
"""
    Caminho para o data frame
"""
dataset = load_data_set()

DATA_RANGE = __get_data_range()
"""Limites do dataset"""

print("Data range: ", DATA_RANGE)

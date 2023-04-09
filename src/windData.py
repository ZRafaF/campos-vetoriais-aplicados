# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import netCDF4 as nc
from typing import List, Tuple
from tqdm import tqdm


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


DATASET_PATH = "data/data_hourly.nc"
"""Caminho para o dataset"""


DATA_RANGE = {"lat": (6, -35), "lon": (-75, -32)}
"""Limites do dataset"""

dataset = load_data_set()

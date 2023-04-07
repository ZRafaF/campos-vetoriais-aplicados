# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import netCDF4 as nc
from typing import List
from typing import Tuple
from tqdm import tqdm
import matplotlib.pyplot as plt


class FormattedData:
    def __init__(self, lat: float, lon: float, u10: float, v10: float):
        self.lat = lat
        self.lon = lon

        # Componente do vento horizontal em m/s
        self.u10 = u10

        # Componente do vento vertical em m/s
        self.v10 = v10


# Carrega o dataset de um arquivo
def load_data_set() -> List[float]:
    return nc.Dataset(DATASET_PATH)


# Retorna as variáveis presentes no dataset
def get_variables() -> List[float]:
    return dataset.variables


def get_keys():
    return dataset.variables.keys()


# Retorna um iterador das latitudes
def get_latitude_list() -> List[float]:
    return dataset.variables["latitude"][:]


# Retorna um iterador das longitudes
def get_longitude_list() -> List[float]:
    return dataset.variables["longitude"][:]


# Retorna um iterador da velocidade do vento no componente v "latitudinal"
def get_v10_list() -> List[float]:
    return dataset.variables["v10"][0]


# Retorna um iterador da velocidade do vento no componente u "longitudinal"
def get_u10_list() -> List[float]:
    return dataset.variables["u10"][0]


# Retorna uma lista de objetos do tipo FormattedData
def format_dataset():
    print("Formatando o dataset...")

    u10_list = get_u10_list()
    v10_list = get_v10_list()

    formatted_list: List[FormattedData] = []

    progress_bar = tqdm(get_latitude_list())

    for idx_lat, lat in enumerate(get_latitude_list()):
        for idx_lon, lon in enumerate(get_longitude_list()):
            u10 = u10_list[idx_lat][idx_lon]
            v10 = v10_list[idx_lat][idx_lon]
            formatted_data = FormattedData(lat, lon, u10, v10)
            formatted_list.append(formatted_data)
        progress_bar.update(1)
    progress_bar.close()
    return formatted_list


def get_formatted_dataset() -> List[FormattedData]:
    return formatted_dataset


def print_dataset() -> None:
    for i in formatted_dataset:
        print("lat: ", i.lat, " lon: ", i.lon, " u10: ", i.u10, " v10: ", i.v10)


# Retorna o numero mais próximo a cada 0.25
def __round_num(num: float) -> float:
    remaining = num % 0.25
    return num - remaining


def get_nearest_point_index(lat: float, lon: float) -> Tuple[float, float]:
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
        print(get_latitude_list()[idx])
        if get_latitude_list()[idx] == closest_lat:
            lat_idx = idx
            break

    # Checando longitude
    for idx, lon in enumerate(get_longitude_list()):
        if get_longitude_list()[idx] == closest_lon:
            lon_idx = idx
            break

    return (lat_idx, lon_idx)


DATA_SET_HAS_BEEN_MADE = False

# Caminho para o dataset
DATASET_PATH = "data/data.nc"

# Limites do dataset
DATA_RANGE = {"lat": (6, -35), "lon": (-75, -32)}

dataset = load_data_set()
<<<<<<< HEAD
formatted_dataset = get_formatted_dataset()
plt.show()

=======


formatted_dataset = format_dataset()
>>>>>>> 0457125c7a4b996e2b6d2e53acc75edd26224616

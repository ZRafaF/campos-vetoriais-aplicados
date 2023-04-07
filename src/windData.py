import netCDF4 as nc
from typing import List


class FormattedData:
    def __init__(self, lat: float, lon: float, u10: float, v10: float):
        self.lat = lat
        self.lon = lon
        self.u10 = u10
        self.v10 = v10


# Carrega o dataset de um arquivo
def load_data_set() -> List[float]:
    return nc.Dataset(DATASET_PATH)


# Retorna as variáveis presentes no dataset
def get_variables() -> List[float]:
    return dataset.variables


# Retorna um iterador das latitudes
def get_latitude_list() -> List[float]:
    return dataset.variables["latitude"]


# Retorna um iterador das longitudes
def get_longitude_list() -> List[float]:
    return dataset.variables["longitude"]


# Retorna um iterador da velocidade do vento no componente v "latitudinal"
def get_v10_list() -> List[float]:
    return dataset.variables["v10"][0][0]


# Retorna um iterador da velocidade do vento no componente u "longitudinal"
def get_u10_list() -> List[float]:
    return dataset.variables["u10"][0][0]


# Retorna uma lista de objetos do tipo FormattedData
def get_formatted_dataset() -> List[FormattedData]:
    lon_list = get_longitude_list()
    u10_list = get_u10_list()
    v10_list = get_v10_list()

    formatted_list: List[FormattedData] = []

    for idx, lat in enumerate(get_latitude_list()):
        lon = lon_list[idx]
        u10 = u10_list[idx]
        v10 = v10_list[idx]
        formatted_data = FormattedData(lat, lon, u10, v10)
        formatted_list.append(formatted_data)

    return formatted_list


def print_dataset() -> None:
    for i in formatted_dataset:
        print("lat: ", i.lat, " lon: ", i.lon, " u10: ", i.u10, " v10: ", i.v10)


DATASET_PATH = "data/data.nc"
dataset = load_data_set()
formatted_dataset = get_formatted_dataset()

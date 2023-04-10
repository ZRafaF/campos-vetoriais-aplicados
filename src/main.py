# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import windData as wd
import configparser
import pathfinding_n as pf
import plotVectorField as pvf
import newAlgo
import numpy as np

CONFIG_PATH = "config.ini"


def load_config_file():
    """Carrega as variáveis do arquivo 'config.ini'"""

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # Criando uma dicionário global
    global config_data
    config_data = {}

    # Pontos são guardados em uma tuple
    config_data["point_1"] = (
        config.getfloat("DEFAULT", "point_1_lat"),
        config.getfloat("DEFAULT", "point_1_lon"),
    )
    config_data["point_2"] = (
        config.getfloat("DEFAULT", "point_2_lat"),
        config.getfloat("DEFAULT", "point_2_lon"),
    )
    config_data["radius"] = config.getfloat("DEFAULT", "radius")

    """ Exemplo de utilização
    latitude_point_1 = config_data["point_1"][0]
    """


if __name__ == "__main__":
    load_config_file()
    dataset = wd.get_formatted_dataset()

    start = (config_data["point_1"][0], config_data["point_1"][1])
    goal = (config_data["point_2"][0], config_data["point_2"][1])
    """
    print(path)
    path = pf.pathField(
        config_data["point_1"][0],
        config_data["point_1"][1],
        config_data["point_2"][0],
        config_data["point_2"][1],
    )
    """
    path = newAlgo.find_path(start, goal, dataset)
    # path = pf.pathField(start[0], start[1], goal[0], goal[1])
    print(path)
    pvf.plot_vector_field_and_path(dataset, np.array([start, goal]))
    # pvf.plot_vector_field_and_path(dataset, path)
    input("Aperte enter para encerrar...")

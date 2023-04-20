# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import windData as wd
import configparser
import plotVectorField as pvf
import networkx as nx
import matplotlib as plt
import study

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


def get_start_goal() -> tuple:
    start = (
        config_data["point_1"][0],
        config_data["point_1"][1],
    )

    goal = (
        config_data["point_2"][0],
        config_data["point_2"][1],
    )
    return (start, goal)


def get_radius() -> float:
    return config_data["radius"]


if __name__ == "__main__":
    load_config_file()
    dataset = wd.get_formatted_dataset()

    start, goal = get_start_goal()

    graph = wd.load_data_frame()

    G = study.get_G(graph)

    # path = study.get_shortest_path(G, start, goal)

    path = study.get_shortest_path_in_radius(start, get_radius(), G)
    pvf.plot_radius(start, get_radius())
    pvf.plot_vector_field(dataset)

    path_2d = study.get_path_2d_from_1d(path)

    print(study.get_path_2d_cost(path_2d))

    pvf.plot_path_smooth(path_2d)

    pvf.show_plot()

    input("Aperte enter para encerrar...")

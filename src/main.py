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

    pvf.plot_vector_field(dataset)

    """
    # Calculando caminho
    path = pf.pathField(
        config_data["point_1"][0],
        config_data["point_1"][1],
        config_data["point_2"][0],
        config_data["point_2"][1],
    )
    
    # Plotando os pontos iniciais e finais e ligando eles
    pvf.plot_path(
        (
            [config_data["point_1"][1], config_data["point_1"][0]],
            [config_data["point_2"][1], config_data["point_2"][0]],
        ),
        color="b",
    )
    """
    # plot start
    pvf.plot_point(
        (
            config_data["point_1"][1],
            config_data["point_1"][0],
        ),
        color="b",
    )

    # plot goal
    pvf.plot_point(
        (
            config_data["point_2"][1],
            config_data["point_2"][0],
        ),
        color="g",
    )

    # pvf.plot_path(path, "r")

    pvf.show_plot()
    input("Aperte enter para encerrar...")

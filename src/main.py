# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import windData as wd
import configparser
import pathfinding_n as pf
import plotVectorField as pvf
import networkx as nx
import pandas as pd


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

    start = (
        config_data["point_1"][0],
        config_data["point_1"][1],
    )

    goal = (
        config_data["point_2"][0],
        config_data["point_2"][1],
    )

    # path = newAlgo.find_path(start, goal, dataset)

    # weighted_matrix, start_idx, goal_idx = wd.make_weighted_matrix(start, goal)

    graph = wd.load_data_frame()

    G = nx.from_pandas_edgelist(
        graph, source="source", target="target", edge_attr="weight"
    )

    start_lat_idx, start_lon_idx = wd.get_nearest_point_index(start[0], start[1])
    goal_lat_idx, goal_lon_idx = wd.get_nearest_point_index(goal[0], goal[1])
    print(start, goal)
    path = nx.shortest_path(
        G,
        source=wd.get_1d_from_2d(start_lat_idx, start_lon_idx),
        target=wd.get_1d_from_2d(goal_lat_idx, goal_lon_idx),
        weight="weight",
        method="dijkstra",
    )

    """
    
    pos = nx.spring_layout(G)
    weights = nx.get_edge_attributes(G, "weight").values()

    nx.draw(G, pos=pos, with_labels=True, node_size=2, width=list(weights))
    nx.draw(G, pos=pos, with_labels=True, node_size=2, )
    """

    """
    for point_1d in path:
        point = wd.get_2d_from_1d(point_1d)
        lat = wd.get_latitude_list()[point[1]]
        lon = wd.get_longitude_list()[point[0]]
        pvf.plot_point([lat, lon], "r")
    """

    # pvf.plot_heatmap(weighted_matrix)
    pvf.plot_vector_field(dataset)

    # plot start
    pvf.plot_point(
        start,
        color="b",
    )

    # plot goal
    pvf.plot_point(
        goal,
        color="g",
    )

    def get_lat_lon_from_1d(idx_1d):
        point = wd.get_2d_from_1d(idx_1d)
        lat = wd.get_latitude_list()[point[1]]
        lon = wd.get_longitude_list()[point[0]]
        return (lat, lon)

    path_2d = list(map(lambda x: get_lat_lon_from_1d(x), path))
    pvf.plot_path(path_2d)

    pvf.show_plot()

    input("Aperte enter para encerrar...")

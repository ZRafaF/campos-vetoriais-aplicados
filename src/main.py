# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import configparser
import plotVectorField as pvf
import study

CONFIG_PATH = "config.ini"


def get_start_goal_radius() -> tuple:
    """Carrega as variáveis do arquivo 'config.ini'"""

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    start = (
        config.getfloat("DEFAULT", "point_1_lat"),
        config.getfloat("DEFAULT", "point_1_lon"),
    )

    goal = (
        config.getfloat("DEFAULT", "point_2_lat"),
        config.getfloat("DEFAULT", "point_2_lon"),
    )

    radius = config.getfloat("DEFAULT", "radius")
    return (start, goal, radius)


if __name__ == "__main__":
    start, goal, radius = get_start_goal_radius()

    # study.a_to_b_study(start, goal)
    study.radius_study(start, radius)
    # study.weights_heatmap_study(start, goal)

    pvf.show_plot()

    input("Aperte enter para encerrar...")

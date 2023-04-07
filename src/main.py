# Copyright (c) 2023
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import windData as wd

CONFIG_PATH = "config.ini"


# Carrega as variáveis do arquivo "config.ini"
def load_config_file():
    import configparser

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # Criando uma dicionário global
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
    # wd.print_dataset()
    input("Aperte enter para encerrar...")

# Campos vetoriais aplicados

## *Environment Setup*
Aqui serão apresentados os passos para a criação do *development environment*.

Antes de iniciar será necessário ter instalado Python 3 e pip.

### Criando um *virtual environment*
Instale a biblioteca [virtualenv](https://pypi.org/project/virtualenv/) `python -m pip install --user virtualenv`.

Crie um *virtual environment* chamado "venv" `python -m venv venv`

Inicie o *virtual environment*
* **Windows**: `venv/Scripts/activate`
* **Linux**: `source venv/bin/activate`


## Dependências
Para instalar as dependências `pip install -r requirements.txt`

## Executar
Para executar o arquivo inicie o *shell script* `./run.sh`

## Utilização

### Formato dos dados
Objeto de um dado:
``` python
class FormattedData:
    def __init__(self, lat: float, lon: float, u10: float, v10: float):
        self.lat = lat
        self.lon = lon

        # Componente do vento horizontal em m/s
        self.u10 = u10

        # Componente do vento vertical em m/s
        self.v10 = v10
```

Exemplo de uso
``` python
import windData as wd

# Primeiro cria o dataset formatado
data_list = wd.get_formatted_dataset()

for data in data_list:
    print("latitude: ", data.lat)
```

### Como ler o vento de uma latitude

``` python
import windData as wd

MY_LAT = 2.25
MY_LON = -40.0

my_wind = wd.get_wind_at(MY_LAT, MY_LON)

print(my_wind)
```

result:
`(-5.44604943914179, -2.6166050070843734)`


### Principais funções
* `get_wind_at(lat: float, lon: float)`: Retorna o valor de vento em uma determinada posição.
> Irá levantar uma exceção caso a posição seja invalida

* `get_latitude_list()`: Retorna uma lista com todas as latitudes do dataset.

* `get_longitude_list()`: Retorna uma lista com todas as longitudes do dataset.

* `get_formatted_dataset()`: Retorna uma lista de objetos do tipo `FormattedData`.

* `print_dataset(formatted_dataset: List[FormattedData])`: Imprime na tela o dataset que for passado.


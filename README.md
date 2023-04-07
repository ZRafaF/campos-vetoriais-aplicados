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

## Formato dos dados
``` python
class FormattedData:
    def __init__(self, lat: float, lon: float, u10: float, v10: float):
        self.lat = lat
        self.lon = lon

        # Componente do vento horizontal em m/s
        self.u10 = u10

        # Componente do vento vertical em m/s
        self.v10 = v10

# Exemplo de uso

# Primeiro cria o dataset formatado
wd.format_dataset()

data_list = wd.get_formatted_dataset()

for data in data_list:
    print("latitude: ", data.lat)

```
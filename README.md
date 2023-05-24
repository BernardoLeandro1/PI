# Assistant for Active Ageing at Home
### Repositório para a unidade curricular Projeto em Informática
#### Abstract
** Inserir Abstract **

#### Authors
 Nome | Email | Nmec |
| :---: | :---: | :---: |
| Bernardo Leandro |email@ua.pt  | 98652 |
| Carlos Sena  | email@ua.pt | 81377 |
| Diogo Silva  | diogomfsilva980@ua.pt | 98644 |
| Luís Martins  | email@ua.pt | 98521 |
| Manuel Diaz  | email@ua.pt | 103645 |
| Pedro Coelho  | email@ua.pt | 104247 |

#### Como correr:
**1** - ```python3 -m venv venv```
**2** - ```source venv/bin/activate```
**3** - ```pip install -r requirements.txt```
**4** - ```pip install --upgrade google-api-python-client oauth2client```
**5** - ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
**6** - ```export GOOGLE_APPLICATION_CREDENTIALS="./speechToTextKey.json"```
**7** - ```rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml```
**8** - Novo terminal: ```rasa run actions```
**9** - Novo terminal: ```python3 ./main.py```

#### Website do projeto:
https://bernardoleandro1.github.io/PI/

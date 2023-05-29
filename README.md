# Assistant for Active Ageing at Home
### Repositório para a unidade curricular Projeto em Informática
#### Abstract
Com o envelhecimento da população portuguesa a aumentar e a tornar-se um problema preocupante, é necessário pensar em formas de ajudar a população idosa a manter a sua independência.  Com isto em mente, foi criado o projeto "Casa Viva+", onde o nosso projeto se insere, e que tem como objetivo a manutenção de uma vida digna em casa. Para atingir este objetivo, propõe-se o desenvolvimento de uma casa capaz de auxiliar nas tarefas domésticas, monitorizar a saúde de quem a habita e ajudar na prevenção e reabilitação.
O projeto sobre o qual este relatório incide consiste na criação de um assistente controlado por voz que irá responder aos pedidos dos habitantes da "Casa Viva+". Diferencia-se de outros assistentes por ser mais fácil de utilizar por idosos, tendo sido pensado especificamente para tal, ao contrário, por exemplo, da Siri ou Alexa, que foram desenvolvidos para ser utilizados por grandes massas e com os quais a populações idosa demonstra alguma dificuldade de utilização. 
Através da interação por voz com o assistente, será possível ao habitante fazer a gestão da sua agenda, informar-se sobre a meteorologia, controlar os dispositivos da referida casa, realizar chamadas, obter sugestão de receitas e recomendação de produtos.
Ao terminarmos a implementação da primeira versão do assistente, realizámos alguns testes com possíveis utilizadores reais para, com base nas experiências reais, conseguirmos melhorar o assistente e tornar as interações o mais fluente possível.


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

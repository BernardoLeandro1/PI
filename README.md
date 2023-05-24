# PI
Repositório para a unidade curricular Projeto em Informática

Como correr:
1 - python3 -m venv venv
2 - source venv/bin/activate
3 - pip install -r requirements.txt
4 - pip install --upgrade google-api-python-client oauth2client
5 - pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
6 - export GOOGLE_APPLICATION_CREDENTIALS="./speechToTextKey.json"
7 - rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
8 - Novo terminal: rasa run actions
9 - Novo terminal: python3 ./main.py

Template para Apresentação:
https://slidesgo.com/theme/tech-company-branding-guidelines#position-6&related-1&rs=detail-related

Website do projeto:
https://bernardoleandro1.github.io/PI/

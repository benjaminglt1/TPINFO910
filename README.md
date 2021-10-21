GALLET Benjamin

# TPINFO910
Projet correspondant au TP d'INFO910 - DevOps

# Architecture du projet

- appSources
    - static
    - templates
    - \_\_init\_\_.py
- compose.yaml
- Dockerfile
- requirements.txt
- server.py 

# Configuration pour Docker

## Docker File
```docker
FROM python:latest

WORKDIR /app



COPY . /app
RUN pip3 install -r requirements.txt


CMD ["python3","runserver.py"]
```

## Docker compose
```yaml
version: "3.9"

services:
  db:
    image: mysql
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: "root"

  flaskserver:
    image: flaskapp
    restart: always
    ports:
      - 3333:3333
    depends_on:
      - db

networks:
  demonet:

```

# Installation

## Build flaskserver
```bash
#Dans le dossier principal
$docker build -t flaskapp:latest .
```
## Run app
```bash
#Dans le dossier principal
$docker compose up
```
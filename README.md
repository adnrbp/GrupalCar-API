# Grupal Car API

Grupal Car is an car pooling app to share a trip with friends.

### 1. List of Features 
  (Must)
  - [X] user signup and send verification email
  - [X] user verification endpoint
  - [X] user login
  - [X] only loged users can list public pools and its private pools
  - [ ] add new pools and stablish admin membership

  (Should) 
  - [ ] Ask for public pools via chatbot

  (Nice)
  - [ ] show a map of near pools
  - [ ] send a notification to pool members



## 2. Installation
  GrupalCar requires [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/) to run

  For a development environment run:  

  ```sh
  export COMPOSE_FILE="local.yml"
  $ docker-compose build
  $ docker-compose up
  ```

  For a production environment run:

  ```sh
  export COMPOSE_FILE="production.yml"
  $ docker-compose build
  $ docker-compose up
  ```  


# 3. Load Sample data

    Utilizando archivo .csv:
    ```sh
    $ docker-compose run --rm django python manage.py shell_plus
        In [1]: exec(open('import_data.py').read())     
        In [2]: import_csv('pools.csv') 
    ```

    Utilizando Fixture:
    ```sh
    $ docker-compose run --rm django python manage.py loaddata grupalcar/pools/fixtures/pools.json
    ```

# 4. API Interaction

Listar Pools:
    GET     {{host}}/pools/
        Response:
        {
            "detail": "Authentication credentials were not provided."
        }
Crear una cuenta:
    POST    {{host}}/users/signup/
        Body:
        { 
            "email": "sample_user@example.com",
            "password": "samplePassword7864",
            "password_confirmation": "samplePassword7864",
            "first_name": "Sample",
            "last_name": "User",
            "phone_number": "+56871354687",
            "username":"samuser"
        }

        Response:
        {
            "username": "samuser",
            "first_name": "Sample",
            "last_name": "User",
            "email": "sample_user@example.com",
            "phone_number": "+56871354687"
        }
(Dev: Revisar email/consola "Verification-JWTCode")
Verficiar cuenta:
    POST    {{host}}/users/verify/
        Body:
        {
            "token":"<part-1>.<part-2>.<part-3>"
        }

        Response:
        {
            "message": "Congratulation, now go share some trips!"
        }
Login:
    POST    {{host}}/users/login/
        Body:
        {
            "email":"sample_user@example.com",
            "password":"samplePassword7864"
        }
        Response:
        {
            "user": {
                "username": "samuser",
                "first_name": "Sample",
                "last_name": "User",
                "email": "sample_user@example.com",
                "phone_number": "+56871354687"
            },
            "access_token": "83ee6f500c4fae4ee9509af51c9768XXXXXXXXXX"
        }
Listar Pools:
    GET     {{host}}/pools/
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json

        Response:
        {
        "count": 14,
        "next": "{{host}}/pools/?limit=3&offset=3",
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Facultad de Ciencias, PUCP",
                "slug_name": "pucp-fciencias",
                "about": "",
                "picture": null,
                "trips_offered": 0,
                "trips_taken": 0,
                "verified": true,
                "is_public": true,
                "is_limited": false,
                "members_limit": 0
            },

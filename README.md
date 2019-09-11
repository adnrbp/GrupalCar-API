# Grupal Car API

Grupal Car is an car pooling app to share a trip with friends.

### 1. List of Features 
  (Must)
  - [X] user signup and send verification email
  - [X] user verification endpoint
  - [X] user login
  - [X] only loged users can list public pools and its private pools
  - [X] add new pools and establish admin membership
  - [X] pool creation with optional definition of members limit
  - [X] only admins can edit a pool, and not even the pool admin can delete a pool
  - [X] only users can see their own data and pools
  - [X] users can edit their own profile, includes profile picture
  - [X] list members of a pool
  - [ ] invite users to pools

  (Should) 
  - [ ] Ask for public pools via chatbot
  - [ ] Pools are disabled when all members leave the pool
  - [ ] Next pool admin is assigned by membership seniority

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

  Create an admin:
  ```sh
  $ docker-compose run --rm django python manage.py createsuperuser
  ```

# 3. Load Sample data

    Use the .csv file:
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

List Pools:
    GET     {{host}}/pools/
        Response:
        {
            "detail": "Authentication credentials were not provided."
        }
Create an account:
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
(Dev: Check email/console "Verification-JWTCode")
Verify account:
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
List Pools:
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
Create a Pool:
    POST    {{host}}/pools/
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Body:
        {
            "name": "Meetup Android Perú",
            "slug_name":"meetup-android",
            "about":"Reuniones android mensuales"
        }
        Response:
        {
            "name": "Meetup Android Perú",
            "slug_name": "meetup-android",
            "about": "Reuniones android mensuales",
            "picture": null,
            "trips_offered": 0,
            "trips_taken": 0,
            "verified": false,
            "is_public": true,
            "is_limited": false,
            "members_limit": 0
        }
            },
Create a Pool with members limit:
    POST    {{host}}/pools/
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Body:
        {
            "name": "Meetup django Perú",
            "slug_name":"meetup-django",
            "about":"Reuniones django mensuales",
            "members_limit":10,
            "is_limited":true
        }
        Response:
        { 
            "name": "Meetup django Perú",
            "slug_name": "meetup-django",
            "about": "Reuniones django mensuales",
            "picture": null,
            "trips_offered": 0,
            "trips_taken": 0,
            "verified": false,
            "is_public": true,
            "is_limited": true,
            "members_limit": 10
        }
Update other user Pool:
    PUT     {{host}}/pools/pucp-fciencias/
        Body:
        {
            "name": "F. Ciencias",
            "slug_name": "pucp-fciencias",
            "about": "Facultad de Ciencias"
        }
        Response:
        {
            "detail": "You do not have permission to perform this action."
        }
Update own Pool:
    PUT     {{host}}/pools/meetup-android/
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Body:
        {
            "name": "Meetup Android Lima",
            "slug_name":"meetup-android",
            "about":"Reuniones android mensuales"
        }
        Response:
        {
            "name": "Meetup Android Lima",
            "slug_name": "meetup-android",
            "about": "Reuniones android mensuales",
            "picture": null,
            "trips_offered": 0,
            "trips_taken": 0,
            "verified": false,
            "is_public": true,
            "is_limited": false,
            "members_limit": 0
        }
User detail:
    GET     {{host}}/users/samuser
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Response:
        {
            "user": {
                "username": "samuser",
                "first_name": "Sample",
                "last_name": "User",
                "email": "sample_user@example.com",
                "phone_number": "+56871354687"
            },
            "pools": [
                {
                    "name": "Meetup python Perú",
                    "slug_name": "meetup-python",
                    "about": "Reuniones python mensuales",
                    "picture": null,
                    "trips_offered": 0,
                    "trips_taken": 0,
                    "verified": false,
                    "is_public": true,
                    "is_limited": false,
                    "members_limit": 0
                },
User Update:
    PUT     {{host}}/users/samuser
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Body:
        {
            "email":"sam_user@example.com",
            "username":"samuser"
        }
        Response:
        {
            "username": "samuser",
            "first_name": "Sample",
            "last_name": "User",
            "email": "sam_user@example.com",
            "phone_number": "+56871354687"
        }

Profile partial Update:
    PATCH   {{host}}/users/samuser/profile/
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Body:
        {
            "biography":"a user sample"
        }
        Response:
        {
            "username": "samuser",
            "first_name": "Sample",
            "last_name": "User",
            "email": "sam_user@example.com",
            "phone_number": "+56871354687"
            "profile": {
                "picture": null,
                "biography": "a user sample",
                "trips_taken": 0,
                "trips_offered": 0,
                "reputation": 5.0
            }
        }
    PATCH {{host}}
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Body(multipart/form-data):
            Content-Disposition: form-data; name="picture"; filename="/path/user-icon-profile.png
        Response:
        {
            "username": "samuser",
            "first_name": "Sample",
            "last_name": "User",
            "email": "sam_user@example.com",
            "phone_number": "+56871354687"
            "profile": {
                "picture": "/media/users/pictures/user-icon-profile.png",
                "biography": "a user sample",
                "trips_taken": 0,
                "trips_offered": 0,
                "reputation": 5.0
            }
        }
List pool members
    GET     {{host}}/pools/meetup-android/members/
        Headers:
            Authorization: Token {{access_token}}
            Content-Type: application/json
        Response:
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "user": {
                            "username": "samuser",
                            "first_name": "Sample",
                            "last_name": "User",
                            "email": "sam_user@example.com",
                            "phone_number": "+56871354687"
                            "profile": {
                                "picture": "http://{{host}}/media/users/pictures/default-user-icon-profile_0YNue7K.png",
                                "biography": "a user sample",
                                "trips_taken": 0,
                                "trips_offered": 0,
                                "reputation": 5.0
                            }
                        },
                        "is_admin": true,
                        "is_active": true,
                        "used_invitations": 0,
                        "remaining_invitations": 10,
                        "invited_by": null,
                        "trips_taken": 0,
                        "trips_offered": 0,
                        "joined_at": "2019-01-01T16:26:35.923258-04:00"
                    }
                ]
            }

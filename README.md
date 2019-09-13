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
  - [X] list members of a pool, retrieve members details and disable memberships
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
    HMBooks-API/api-interaction-samples.txt
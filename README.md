# Grupal Car API

Grupal Car is an car pooling app to share a trip with friends.

### 1. List of Features 
  (Must)
  - [X] User signup and send verification email
  - [X] User verification endpoint
  - [X] User login
  - [X] Only loged users can list public pools and its private pools
  - [X] Add new pools and establish admin membership
  - [X] Pool creation with optional definition of members limit
  - [X] Only admins can edit a pool, and not even the pool admin can delete a pool
  - [X] Only users can see their own data and pools
  - [X] Users can edit their own profile, includes profile picture
  - [X] List members of a pool, retrieve members details and disable memberships
  - [X] List all members invited by another user
  - [X] List all invitations available (new and different code for unused) for members 
  - [X] Invite users to pools and add new members (validate code and pool limit)
  - [X] Users can search pools by name and order them
  - [X] By default, list pools ordered by number of members
  - [ ] Create a trip in a pool
  - [ ] List all trips
  - [ ] Edit trip information for passengers
  - [ ] Pool member can join to a trip, and become a passenger
  - [ ] Mark a trip as ended, when it reaches the destination.
  - [ ] Allow passengers to rate the trip

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
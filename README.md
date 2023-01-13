# TODOlist

_This is app that helps users to manage their tasks and planned meetings_

## Technologies:
 - Python 3.10
 - Django 4.0.1
 - Django REST framework 3.14.0
 - Postgres 


## Build and Run in Docker Compose
Create .env file and add config values for connecting to postgres:
 * POSTGRES_DB
 * POSTGRES_USER
 * POSTGRES_PASSWORD

The only requirement to build and run the app from source is Docker. Clone this repo and use Docker Compose to build all the images.
'''
docker compose up --build
'''
Docker compose includes the following containers:
 - A front-end web app in React
 - A back-end web app in Python
 - Container which let you use telegram bot
 - A Postgres database backed by a Docker volume
 - Container which run database migrations

## The TODOlist
The URL for the content is http://localhost:8000/

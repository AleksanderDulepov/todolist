# TODOlist

_This is api that helps users to handle their tasks and meetings_

## Technologies:
 - python 3.10
 - Django 4.0.1
 - Postgres 


## Installation: 
TODOlist requires [python](https://www.python.org/downloads/) v3+ to run.

Install the dependencies:
```sh
pip install -r requirements.txt
```
Create .env file and add config values for connecting to postgres:
 * POSTGRES_DB
 * POSTGRES_USER
 * POSTGRES_PASSWORD

Perform migrations:
```sh
python manage.py migrate
```

And finally start app:
```sh
python manage.py runserver
```

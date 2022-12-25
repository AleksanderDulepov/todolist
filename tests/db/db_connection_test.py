import os

import psycopg2
import pytest
from dotenv import load_dotenv

from todolist import settings
from django.db import connection

dotenv_path = settings.dotenv_path
load_dotenv(dotenv_path)


@pytest.mark.django_db
def test_db_connection():
    try:
        db = psycopg2.connect(host=os.environ.get("DB_HOST"),
                              port=os.environ.get("DB_PORT"),
                              dbname=os.environ.get("POSTGRES_DB"),
                              user=os.environ.get("POSTGRES_USER"),
                              password=os.environ.get("POSTGRES_PASSWORD")
                              )
    except:
        raise AssertionError("Database is unavailable")

    assert db


    # cursor = connection.cursor()
    # query='''pg_isready -d todolist -U todolist'''
    # cursor.execute(query)
    # row_data=cursor.fetchall()
    # print(row_data)



@pytest.mark.django_db
def test_db_connection_one_more():
    is_connection_ok = connection.ensure_connection()
    assert is_connection_ok==None

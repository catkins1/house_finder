import pytest
import pymongo

from src.get_google_data import database_connect

def test_get_db_connection():
    """
    This should be able to connect to the mongo db and return a list of database names.
    """
    assert isinstance(database_connect.db_connect(), pymongo.database.Database)
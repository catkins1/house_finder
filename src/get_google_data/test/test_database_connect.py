import pytest

from src.get_google_data import database_connect

def test_client_response_ok():
    """
    This should be able to connect to the mongo db and return a list of database names.
    """
    assert isinstance(database_connect.client.list_database_names(), list)
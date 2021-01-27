import pymongo
import os

def db_connect():
    """
    Gets connection to the correct Mongo database

    Returns:
        pymongo.database.Database: The housefinder database

    """
    client = pymongo.MongoClient(
        "mongodb://localhost:27017/",#?compressors=disabled&gssapiServiceName=mongodb",
        username=os.environ["MONGO_INITDB_ROOT_USERNAME"],
        password=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
    )

    return client["house_finder"]



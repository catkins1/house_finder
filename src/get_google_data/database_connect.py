import pymongo
import os


client = pymongo.MongoClient(
    "mongodb://localhost:27017/",#?compressors=disabled&gssapiServiceName=mongodb",
    username=os.environ["MONGO_INITDB_ROOT_USERNAME"],
    password=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
)

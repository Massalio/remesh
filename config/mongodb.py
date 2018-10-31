import os
from pymongo import MongoClient

mongo_uri = "mongodb://rocky-headland-53719.herokuapp.com/api"
if "MONGO_URL" in os.environ:
    mongo_uri = os.environ['MONGO_URL'] + ":" + os.environ['MONGO_PORT']

mongo = MongoClient(mongo_uri)
db = mongo['lio_server']

MONGO_DB_NAME = "lio_server"

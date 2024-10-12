import pymongo
from config.config import mongo_config


def create():
    key = mongo_config.read_config()
    client = pymongo.MongoClient(key["link"])

    return client
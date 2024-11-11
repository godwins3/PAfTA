import pymongo
from config.config import mongo_config
from pymongo.errors import ConfigurationError


def create():
    try:
        key = mongo_config()
        client = pymongo.MongoClient(key["link"], serverSelectionTimeoutMS=5000)
        # Trigger a server selection to verify the connection
        client.server_info()
        return client
    except ConfigurationError as ce:
        print(f"MongoDB Configuration Error: {ce}")
        print("Please check your MongoDB connection string in the config file.")
        return None
    except pymongo.errors.ServerSelectionTimeoutError:
        print("Failed to connect to MongoDB server. Please check your network connection and MongoDB server status.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

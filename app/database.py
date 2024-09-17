from pymongo import MongoClient

from .config import settings


client = MongoClient(settings.DATABASE_URL)
db = client[settings.db_name]
form_collection = db[settings.form_collection_name]
counter_collection = db[settings.counter_collection_name]

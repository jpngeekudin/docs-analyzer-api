from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_client = AsyncMongoClient(os.getenv('MONGO_URL'))
db = mongo_client[os.getenv('MONGO_DB')]
history_collection = db["chats"]
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["ai_inbox"]
items_collection = db["items"]
chunks_collection = db["chunks"]

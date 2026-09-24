from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client[os.getenv("DB_NAME")]

products_collection = db["products"]
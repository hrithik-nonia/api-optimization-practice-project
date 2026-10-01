from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"),
                            minPoolSize=10,  # connection polling connection ko live rakhta hai close nahi karta hai
                            maxPoolSize=300)
db = client[os.getenv("DB_NAME")]

products_collection = db["products"]
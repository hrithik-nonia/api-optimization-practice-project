import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import random

categories = ["Electronics", "Clothing", "Books", "Sports", "Home", "Beauty"]
brands = ["Samsung", "Nike", "Apple", "Sony", "Adidas", "LG", "Puma"]

async def seed():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["product_db"]
    col = db["products"]

    await col.delete_many({})  # clear old data

    products = []
    for i in range(100_000):  # 1 lakh products
        products.append({
            "name": f"Product {i}",
            "category": random.choice(categories),
            "price": round(random.uniform(10, 10000), 2),
            "stock": random.randint(0, 1000),
            "rating": round(random.uniform(1, 5), 1),
            "brand": random.choice(brands),
            "description": f"Description for product {i} " * 5,
            "created_at": datetime.utcnow()
        })

    # Batch insert — 1000 at a time
    for i in range(0, len(products), 1000):
        await col.insert_many(products[i:i+1000])
        print(f"Inserted {i+1000} products...")

    print("✅ Seeding complete!")
    client.close()

asyncio.run(seed())
from fastapi import APIRouter, Query
from app.database import products_collection
from app.models import ProductsResponse, CreateProduct, ProductResponse, ProductAddInDb, Product
from datetime import datetime, timezone
import random

router = APIRouter()

@router.get("/products", response_model=ProductsResponse)
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    sort_by: str = Query("created_at"),
    order: int = Query(-1)  
):
    # Build filter query
    query = {}
    if category:
        query["category"] = category
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price

    skip = (page - 1) * limit

    # DB se data fetch karo
    cursor = products_collection.find(query)
    cursor = cursor.sort(sort_by, order).skip(skip).limit(limit)

    products = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        products.append(doc)

    total = await products_collection.count_documents(query)

    return ProductsResponse(
        total=total,
        page=page,
        limit=limit,
        products=products
    )
    
    
@router.post("/create-product", response_model=ProductResponse)
async def create_product(data: CreateProduct):
    rating = random.randint(1, 5)
    product = ProductAddInDb(
        name= data.name,
        category= data.category,
        price= data.price,
        stock= data.stock,
        brand= data.brand,
        description= data.description,
        created_at= datetime.now(timezone.utc),
        rating= rating
    )
    response = await products_collection.insert_one(
            product.model_dump()
        )
    
    return ProductResponse(
        message= "Product Added",
        product = Product(
            id= str(response.inserted_id),
            name= data.name,
            category= data.category,
            price= data.price,
            stock= data.stock,
            rating= rating,
            brand= data.brand,
            description= data.description,
            created_at= datetime.now(timezone.utc)
        )
    )
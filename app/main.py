from fastapi import FastAPI
from app.routes.product import router as product_route
from contextlib import asynccontextmanager
from app.database import products_collection



@asynccontextmanager
async def lifespan(app: FastAPI):
    await products_collection.create_index(
        [
            ("created_at", -1),
            ("price", 1)
        ],
        name="created_at_desc"
    )

    yield

app = FastAPI(title="Product API", lifespan=lifespan)
app.include_router(product_route, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
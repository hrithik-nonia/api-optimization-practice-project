import uvloop
uvloop.install()
from fastapi import FastAPI
from app.routes.product import router as product_route
from contextlib import asynccontextmanager
from app.database import products_collection
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.rate_limit import limiter
from app.database import client
from app.redis_client import redis_client



@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup: MongoDB indexes
    await products_collection.create_index(
        [("created_at", -1)],
        name="created_at_desc"
    )

    await products_collection.create_index(
        [("price", 1)],
        name="price_asc"
    )

    # Startup: Redis connection check
    await redis_client.ping()

    print("MongoDB and Redis connected")

    yield

    # Shutdown: Close Redis
    await redis_client.aclose()

    # Shutdown: Close MongoDB
    client.close()

    print("MongoDB and Redis connections closed")
    


app = FastAPI(title="Product API", lifespan=lifespan)

# add rate limeter
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# add GZip middle ware
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

# include route
app.include_router(product_route, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
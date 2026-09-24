from fastapi import FastAPI
from app.routes.product import router as product_route

app = FastAPI(title="Product API")
app.include_router(product_route, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
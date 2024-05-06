from main import app
from fastapi import HTTPException, Request
from main.schemas.response import ResponseList, ResponseDict
from main.schemas.product import CreateProductSchema
from main.utils.auth import authenticate_user
from main.utils.product import get_products, create_new_product, get_product


@app.get("/api/products", response_model=ResponseList, tags=["products"])
async def read_products(request: Request):
    await authenticate_user(request)
    data = await get_products()
    return {"result": True, "message": "Успешно, список товаров был просмотрен!", "data": data}


@app.post("/api/products", response_model=ResponseDict, tags=["products"])
async def create_product(product: CreateProductSchema, request: Request):
    await authenticate_user(request)
    await create_new_product(product=product.name_product)
    return {"result": True, "message": f"Вы успешно добавили товар - {product.name_product.lower()}!", "data": {}}


@app.get("/api/products/{product_id}", response_model=ResponseDict, tags=["products"])
async def read_product(product_id: int, request: Request):
    await authenticate_user(request)
    data = await get_product(product_id=product_id)
    return {"result": True, "message": "Успешно, товар был просмотрен!", "data": data}

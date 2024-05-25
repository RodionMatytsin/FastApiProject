from main import app
from fastapi import Request
from main.schemas.response import DefaultResponse
from main.schemas.product import CreateProductSchema
# from main.utils.auth import authenticate_user
# from main.utils.product import get_products, create_new_product, get_product


@app.get("/api/products", status_code=200, tags=["Products"])
async def read_products(request: Request):
    # await authenticate_user(request)
    # data = await get_products()
    # return {"result": True, "message": "Успaешно, список товаров был просмотрен!", "data": data}
    return DefaultResponse()


@app.post("/api/products", status_code=200, tags=["Products"])
async def create_product(product: CreateProductSchema, request: Request):
    # await authenticate_user(request)
    # await create_new_product(product=product.name_product)
    # return {"result": True, "message": f"Вы успешно добавили товар - {product.name_product.lower()}!", "data": {}}
    return DefaultResponse()


@app.get("/api/products/{product_id}", status_code=200, tags=["Products"])
async def read_product(product_id: int, request: Request):
    # await authenticate_user(request)
    # data = await get_product(product_id=product_id)
    # return {"result": True, "message": "Успешно, товар был просмотрен!", "data": data}
    return DefaultResponse()

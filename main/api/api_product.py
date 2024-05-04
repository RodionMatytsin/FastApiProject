from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.schemas.product import CreateProductSchema
from main.utils.auth import authenticate_user
from main.utils.product import get_products, create_new_product, get_product


@app.get("/api/products", tags=["products"])
async def read_products(request: Request):
    if await authenticate_user(request):
        data = await get_products()
        content = {"result": True, "message": "Успешно, список товаров был просмотрен!", "data": data}
        return JSONResponse(content=content)


@app.post("/api/products", tags=["products"])
async def create_product(product: CreateProductSchema, request: Request):
    if await authenticate_user(request):
        await create_new_product(product=product.name_product)
        content = {"result": True, "message": f"Вы успешно добавили товар - {product.name_product.lower()}!",
                   "data": product.name_product}
        return JSONResponse(content=content)


@app.get("/api/products/{product_id}", tags=["products"])
async def read_product(product_id: int, request: Request):
    if await authenticate_user(request):
        data = await get_product(product_id=product_id)
        content = {"result": True, "message": "Успешно, товар был просмотрен!", "data": data}
        return JSONResponse(content=content)

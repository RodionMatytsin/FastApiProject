from main import app
from fastapi import Depends
from main.utils.auth import get_current_user
from main.schemas.response import DefaultResponse
from main.schemas.product import CreateProductSchema
from main.utils.product import get_products, create_new_product, get_product


@app.get("/api/products", dependencies=[Depends(get_current_user)], status_code=200, tags=["Products"])
async def read_products():
    return DefaultResponse(data=await get_products())


@app.post("/api/products", dependencies=[Depends(get_current_user)], status_code=200, tags=["Products"])
async def create_product(product: CreateProductSchema):
    return DefaultResponse(data=await create_new_product(name_product=product.name_product))


@app.get("/api/products/{product_id}", dependencies=[Depends(get_current_user)], status_code=200, tags=["Products"])
async def read_product(product_id: int):
    return DefaultResponse(data=await get_product(product_id=product_id))

from fastapi import HTTPException
from main.models.fake_db import listProducts, listUsers


async def get_products() -> list:
    return sorted(listProducts, key=lambda x: x["product_id"])


async def create_new_product(product: str) -> dict:
    last_product_id = max([product["product_id"] for product in listProducts]) + 1 if listUsers else 0
    new_product = {"product_id": last_product_id, "name_product": product}
    listProducts.append(new_product)
    return new_product


async def get_product(product_id: int) -> dict:
    product = next((product for product in listProducts if product["product_id"] == product_id), None)
    if product is None:
        detail = {"result": False, "message": "Ошибка, товар с таким идентификатором не найден!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)
    return product

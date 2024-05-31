from fastapi import HTTPException
from main.models.database import Products


async def get_products() -> list:
    return [dict(id=i[0], name_product=i[1]) for i in await Products.get_products_()]


async def create_new_product(name_product: str) -> str:
    await Products.add_product_(name_product_=name_product)
    return "Товар был успешно создан!"


async def get_product(product_id: int) -> dict:
    product = await Products.get_product_(product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail={"result": False, "message": "Ошибка, товар с таким идентификатором не найден!", "data": {}}
        )
    return dict(id=product.id, name_product=product.name_product)

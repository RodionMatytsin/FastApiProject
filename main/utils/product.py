from fastapi import HTTPException
from main.utils.another import escape
from main.models.database import query_execute


async def get_products():
    data = await query_execute(
        query_text=f'SELECT '
                   f'P.id, '
                   f'P.name_product '
                   f'FROM "Products" AS P '
                   f'ORDER BY P.id',
        fetch_all=True,
        type_query='read'
    )
    return [dict(id=row[0], username=row[1]) for row in data]


async def create_new_product(product: str):
    new_product = await query_execute(
        query_text=f'INSERT INTO "Products" (name_product) '
                   f'VALUES (\'{escape(product)}\')',
        fetch_all=False,
        type_query='insert'
    )
    return new_product


async def get_product(product_id: int):
    product = await query_execute(
        query_text=f'SELECT '
                   f'P.id, '
                   f'P.name_product '
                   f'FROM "Products" AS P '
                   f'WHERE P.id = {product_id}',
        fetch_all=False,
        type_query='read'
    )
    if product is None:
        detail = {"result": False, "message": "Ошибка, товар с таким идентификатором не найден!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)
    return product

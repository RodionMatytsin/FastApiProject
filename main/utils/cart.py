from main.utils.product import get_product
from main.models.database import query_execute


async def get_cart(user_id: int):
    data = await query_execute(
        query_text=f'SELECT '
                   f'C.id, '
                   f'C.product_id,'
                   f'C.user_id '
                   f'FROM "Carts" AS C '
                   f'WHERE C.user_id = {user_id[0]} '
                   f'ORDER BY C.id',
        fetch_all=True,
        type_query='read'
    )
    return [dict(id=i[0], product_id=i[1], user_id=i[2]) for i in data]


async def add_product_to_cart_by_id(product_id: int, user_id: int):
    product = await get_product(product_id=product_id)
    new_product_in_cart = await query_execute(
        query_text=f'INSERT INTO "Carts" (product_id, user_id) '
                   f'VALUES ({product[0]}, {user_id[0]})',
        fetch_all=False,
        type_query='insert'
    )
    return new_product_in_cart


async def add_order_from_cart(user_id: int):
    orders = []
    carts = await get_cart(user_id=user_id)
    for cart in carts:
        order = await query_execute(
            query_text=f'INSERT INTO "Orders" (cart_id, product_id, user_id) '
                       f'VALUES ({cart.get("id")}, {cart.get("product_id")}, {user_id[0]})',
            fetch_all=False,
            type_query='insert'
        )
        orders.append(order)
    # for _ in range(len(orders)):
    #     await query_execute(
    #         query_text=f'DELETE FROM "Carts" WHERE user_id = {user_id[0]}',
    #         fetch_all=False,
    #         type_query='delete'
    #     )
    return orders

from main.models.database import query_execute


async def get_order(user_id: int):
    data = await query_execute(
        query_text=f'SELECT '
                   f'O.id, '
                   f'O.cart_id,'
                   f'O.product_id,'
                   f'O.user_id '
                   f'FROM "Orders" AS O '
                   f'WHERE O.user_id = {user_id[0]} '
                   f'ORDER BY O.id',
        fetch_all=True,
        type_query='read'
    )
    return [dict(id=i[0], cart_id=i[1], product_id=i[2], user_id=i[3]) for i in data]

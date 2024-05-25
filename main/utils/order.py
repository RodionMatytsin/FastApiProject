# from main.models.database import query_execute
#
#
# async def get_order(user_id: int):
#     data = await query_execute(
#         query_text=f'SELECT P.name_product AS "name_product", O.user_id AS "user_id" '
#                    f'FROM "Orders" AS O '
#                    f'INNER JOIN "Products" AS P ON P.id = O.product_id '
#                    f'WHERE O.user_id = {user_id[0]} '
#                    f'ORDER BY O.product_id',
#         fetch_all=True,
#         type_query='read'
#     )
#     return [dict(name_product=i[0], user_id=i[1]) for i in data]

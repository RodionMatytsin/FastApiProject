# from main.utils.product import get_product
# from main.models.database import query_execute
#
#
# async def get_cart(user_id: int):
#     data = await query_execute(
#         query_text=f'SELECT P.name_product AS "name_product", C.user_id AS "user_id" '
#                    f'FROM "Carts" AS C '
#                    f'INNER JOIN "Products" AS P ON P.id = C.product_id '
#                    f'WHERE C.user_id = {user_id[0]} '
#                    f'ORDER BY C.product_id',
#         fetch_all=True,
#         type_query='read'
#     )
#     return [dict(name_product=i[0], user_id=i[1]) for i in data]
#
#
# async def add_product_to_cart_by_id(product_id: int, user_id: int):
#     product = await get_product(product_id=product_id)
#     new_product_in_cart = await query_execute(
#         query_text=f'INSERT INTO "Carts" (product_id, user_id) '
#                    f'VALUES ({product[0]}, {user_id[0]})',
#         fetch_all=False,
#         type_query='insert'
#     )
#     return new_product_in_cart
#
#
# async def add_order_from_cart(user_id: int):
#     orders = []
#     data = await query_execute(
#         query_text=f'SELECT '
#                    f'C.id, '
#                    f'C.product_id, '
#                    f'C.user_id '
#                    f'FROM "Carts" AS C '
#                    f'WHERE C.user_id = {user_id[0]}',
#         fetch_all=True,
#         type_query='read'
#     )
#     carts = [dict(id=i[0], product_id=i[1], user_id=[2]) for i in data]
#     for cart in carts:
#         order = await query_execute(
#             query_text=f'INSERT INTO "Orders" (cart_id, product_id, user_id) '
#                        f'VALUES ({cart.get("id")}, {cart.get("product_id")}, {user_id[0]})',
#             fetch_all=False,
#             type_query='insert'
#         )
#         orders.append(order)
#     # await query_execute(
#     #     query_text=f'DELETE FROM "Carts" AS C WHERE C.user_id = {user_id[0]}',
#     #     fetch_all=False,
#     #     type_query='delete'
#     # )
#     return orders

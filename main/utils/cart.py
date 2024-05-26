from main.utils.product import get_product
from main.models.database import Carts, Orders


async def get_cart(user_id: int):
    return [dict(name_product=i[0], user_id=i[1]) for i in await Carts.get_cart_(user_id=user_id)]


async def add_product_to_cart_by_id(product_id: int, user_id: int):
    product = await get_product(product_id=product_id)
    return await Carts.add_cart_(product_id_=product["id"], user_id_=user_id)


async def add_order_from_cart(user_id: int):
    orders = []
    cart_user = [dict(id=i[0], product_id=i[1], user_id=i[2]) for i in await Carts.get_all_cart_(user_id=user_id)]
    for cart in cart_user:
        order = await Orders.add_order_(cart_id=cart["id"], product_id_=cart["product_id"], user_id_=user_id)
        orders.append(order)
    # for i in range(len(orders)):
    #     await Orders.delete_all_orders_for_cart_(user_id=user_id)
    #     await Carts.delete_cart_(user_id=user_id)
    return orders

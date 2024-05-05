from fastapi import HTTPException
from main.utils.product import get_product
from main.models.fake_db import listOfProductInCart, listOrder


async def get_cart(user_id: int) -> list:
    data = [
        {
            "product_id": cart["product_id"],
            "name_product": cart["name_product"],
            "user_id": cart["user_id"]
        }
        for cart in sorted(listOfProductInCart, key=lambda x: x["product_id"])
        if cart["user_id"] == user_id
    ]
    return data


async def add_product_to_cart(product_id: int, name_product: str, user_id: int) -> dict:
    new_product_in_cart = {"product_id": product_id, "name_product": name_product, "user_id": user_id}
    listOfProductInCart.append(new_product_in_cart)
    return new_product_in_cart


async def add_product_to_cart_by_id(product_id: int, user_id: int) -> dict:
    product = await get_product(product_id=product_id)
    new_product = await add_product_to_cart(
        product_id=product["product_id"],
        name_product=product["name_product"],
        user_id=user_id
    )
    return new_product


async def add_an_order_from_the_cart(user_id: int) -> list:
    data = [listOrder.append(cart) for cart in listOfProductInCart if cart["user_id"] == user_id]
    for _ in range(len(data)):
        [listOfProductInCart.remove(cart) for cart in listOfProductInCart if cart["user_id"] == user_id]
    return data

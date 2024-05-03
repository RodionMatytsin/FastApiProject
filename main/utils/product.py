from main.models.fake_db import listProducts, listOfProductInCart, listUsers


async def create_new_product(product: str) -> dict:
    last_product_id = max([product["product_id"] for product in listProducts]) + 1 if listUsers else 0
    new_product = {"product_id": last_product_id, "name_product": product}
    listProducts.append(new_product)
    return new_product


async def get_product_by_id(product_id: int) -> dict:
    return next((product for product in listProducts if product["product_id"] == product_id), None)


async def add_product_to_cart(product_id: int, name_product: str, user_id: int) -> dict:
    new_product_in_cart = {"product_id": product_id, "name_product": name_product, "user_id": user_id}
    listOfProductInCart.append(new_product_in_cart)
    return new_product_in_cart

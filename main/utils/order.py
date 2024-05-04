from main.models.fake_db import listOrder


async def get_order(user_id: int) -> list:
    data = [
        {
            "product_id": order["product_id"],
            "name_product": order["name_product"],
            "user_id": order["user_id"]
        }
        for order in sorted(listOrder, key=lambda x: x["product_id"])
        if order["user_id"] == user_id
    ]
    return data

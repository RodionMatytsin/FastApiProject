from main.models.database import Orders


async def get_order(user_id: int) -> list:
    return [dict(name_product=i[0], user_id=i[1]) for i in await Orders.get_order_(user_id=user_id)]

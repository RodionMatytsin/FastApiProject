# from main import app
# from fastapi import Request
# from main.schemas.response import DefaultResponse
# # from main.utils.auth import authenticate_user, get_user_id
# # from main.utils.cart import get_cart, add_product_to_cart_by_id, add_order_from_cart
#
#
# @app.get("/api/cart", status_code=200, tags=["Cart"])
# async def read_cart(request: Request):
#     # await authenticate_user(request)
#     # data = await get_cart(user_id=await get_user_id(request))
#     # return {"result": True, "message": "Просмотр корзины совершенно успешно!", "data": data}
#     return DefaultResponse()
#
#
# @app.post("/api/cart/{product_id}", status_code=200, tags=["Cart"])
# async def create_product_to_cart_by_id(product_id: int, request: Request):
#     # await authenticate_user(request)
#     # data = await add_product_to_cart_by_id(product_id=product_id, user_id=await get_user_id(request))
#     # return {"result": True, "message": f'Вы успешно добавили товар в корзину!', "data": data}
#     return DefaultResponse()
#
#
# @app.post("/api/cart", status_code=200, tags=["Cart"])
# async def create_an_order_from_the_cart(request: Request):
#     # await authenticate_user(request)
#     # data = await add_order_from_cart(user_id=await get_user_id(request))
#     # return {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
#     return DefaultResponse()

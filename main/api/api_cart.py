from main import app
from fastapi import HTTPException, Request
from main.utils.auth import authenticate_user, get_user_id
from main.utils.cart import get_cart, add_product_to_cart_by_id, add_an_order_from_the_cart


@app.get("/api/cart", tags=["cart"])
async def read_cart(request: Request):
    if await authenticate_user(request):
        data = await get_cart(user_id=await get_user_id(request))
        return {"result": True, "message": "Просмотр корзины совершенно успешно!", "data": data}


@app.post("/api/cart/{product_id}", tags=["cart"])
async def create_product_to_cart_by_id(product_id: int, request: Request):
    if await authenticate_user(request):
        data = await add_product_to_cart_by_id(product_id=product_id, user_id=await get_user_id(request))
        return {"result": True, "message": f'Вы успешно добавили товар - {data.get("name_product").lower()} в корзину!',
                "data": data["name_product"]}


@app.post("/api/cart", tags=["cart"])
async def create_an_order_from_the_cart(request: Request):
    if await authenticate_user(request):
        data = await add_an_order_from_the_cart(user_id=await get_user_id(request))
        return {"result": True, "message": "Заказ был успешно оформлен!", "data": data}

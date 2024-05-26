from main import app
from fastapi import Depends
from main.utils.auth import get_current_user
from main.schemas.response import DefaultResponse
from main.utils.cart import get_cart, add_product_to_cart_by_id


@app.get("/api/cart", status_code=200, tags=["Cart"])
async def read_cart(user=Depends(get_current_user)):
    return DefaultResponse(data=await get_cart(user_id=user.id))


@app.post("/api/cart/{product_id}", status_code=200, tags=["Cart"])
async def create_product_to_cart_by_id(product_id: int, user=Depends(get_current_user)):
    return DefaultResponse(data=await add_product_to_cart_by_id(product_id=product_id, user_id=user.id))


@app.post("/api/cart", status_code=200, tags=["Cart"])
async def create_an_order_from_the_cart(user=Depends(get_current_user)):
    # await authenticate_user(request)
    # data = await add_order_from_cart(user_id=await get_user_id(request))
    # return {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
    return DefaultResponse(data=user.id)

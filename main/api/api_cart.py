from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.utils.auth import get_user_token, get_check_token
from main.utils.cart import get_cart, add_product_to_cart_by_id, add_an_order_from_the_cart


@app.get("/api/cart", tags=["cart"])
async def read_cart(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        data = await get_cart(check_token=check_token)
        content = {"result": True, "message": "Просмотр корзины совершенно успешно!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


@app.post("/api/cart/{product_id}", tags=["cart"])
async def create_product_to_cart_by_id(product_id: int, request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        data = await add_product_to_cart_by_id(product_id=product_id, check_token=check_token)
        content = {"result": True,
                   "message": f'Вы успешно добавили товар - {data.get("name_product").lower()} в корзину!',
                   "data": data["name_product"]}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


@app.post("/api/cart", tags=["cart"])
async def create_an_order_from_the_cart(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        data = await add_an_order_from_the_cart(check_token=check_token)
        content = {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

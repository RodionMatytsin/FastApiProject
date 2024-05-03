from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.utils.auth import get_user_token, get_check_token, get_user_token_by_id
from main.utils.product import get_product_by_id, add_product_to_cart
from main.models.fake_db import listOfProductInCart, listOrder


@app.get("/api/cart", tags=["cart"])
async def read_cart(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        user_id = await get_user_token_by_id(access_token=token)
        data = [
            {
                "product_id": cart["product_id"],
                "name_product": cart["name_product"],
                "user_id": cart["user_id"]
            }
            for cart in sorted(listOfProductInCart, key=lambda x: x["product_id"])
            if cart["user_id"] == user_id
        ]

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
        product = await get_product_by_id(product_id=product_id)
        if product is None:
            detail = {"result": False, "message": "Ошибка, товар с таким идентификатором не найден!", "data": {}}
            raise HTTPException(status_code=404, detail=detail)

        user_id = await get_user_token_by_id(access_token=token)
        new_product = await add_product_to_cart(product_id=product["product_id"],
                                                name_product=product["name_product"], user_id=user_id)

        content = {"result": True,
                   "message": f'Вы успешно добавили товар - {new_product.get("name_product").lower()} в корзину!',
                   "data": new_product["name_product"]}
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
        user_id = await get_user_token_by_id(access_token=token)
        data = [listOrder.append(cart) for cart in listOfProductInCart if cart["user_id"] == user_id]
        for _ in range(len(data)):
            [listOfProductInCart.remove(cart) for cart in listOfProductInCart if cart["user_id"] == user_id]

        content = {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

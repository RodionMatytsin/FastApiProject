import hashlib
from pydantic import UUID4
from fastapi import FastAPI, HTTPException
from fastapi import Request, Cookie, Response, Depends
from starlette.responses import JSONResponse
from schemas import ProductSchema, CartSchema, UserLoginSchema, DefaultResponse, UserSignUp
from fake_db import listUsers, listToken, listProducts, listOrder, listOfProductInCart
from uuid import uuid4
from datetime import datetime, timedelta


app = FastAPI(title="FastAPI")


def hash_password(password: str) -> str:
    h = hashlib.new('sha256')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


@app.get("/api/users", tags=["auth"])
async def read_users():
    content = {"result": True, "message": "Успешно, список пользователей был просмотрен!",
               "data": sorted(listUsers, key=lambda x: x["user_id"])}
    return JSONResponse(content=content)


@app.get("/api/users_token", tags=["auth"])
async def read_users_token():
    data = [{"user_id": token["user_id"],
             "access_token": token["access_token"],
             "expire": token["expire"].isoformat(),
             "datetime_create": token["datetime_create"].isoformat()}
            for token in sorted(listToken, key=lambda x: x["user_id"])]

    content = {"result": True, "message": "Успешно, список токенов был просмотрен!", "data": data}
    return JSONResponse(content=content)


async def get_user(username: str, password: str) -> dict:
    for user in listUsers:
        if user["username"] == username and user["password"] == password:
            return user
    detail = {"result": False, "message": "Ошибка, неверный логин или пароль!", "data": {}}
    raise HTTPException(status_code=404, detail=detail)


async def update_user_token(user_id: int) -> dict:
    check_token = next((token for token in listToken if token["user_id"] == user_id), None)
    if check_token is None:
        new_token = {"user_id": user_id, "access_token": str(uuid4()),
                     "expire": datetime.utcnow() + timedelta(minutes=1), "datetime_create": datetime.utcnow()}
        listToken.append(new_token)
        return new_token
    else:
        if datetime.utcnow() > check_token["expire"]:
            check_token["access_token"] = str(uuid4())
            check_token["expire"] = datetime.utcnow() + timedelta(minutes=1)
            return check_token
        else:
            return check_token


@app.post("/api/login", response_model=DefaultResponse, tags=["auth"])
async def api_login(user: UserLoginSchema, response: Response):
    user = await get_user(username=user.username, password=hash_password(user.password))

    user_token = await update_user_token(user_id=user["user_id"])
    response.set_cookie(key="user_token", value=user_token["access_token"], httponly=True)

    return {"result": True, "message": "Вы успешно авторизовались!", "data": {}}


async def get_user_by_username(username: str) -> dict:
    for user in listUsers:
        if user["username"] == username:
            return user


async def get_user_by_email(email: str) -> dict:
    for user in listUsers:
        if user["email"] == email:
            return user


async def create_new_user(username: str, email: str, password: str) -> dict:
    last_user_id = max([user["user_id"] for user in listUsers]) + 1 if listUsers else 0
    new_user = {"user_id": last_user_id, "username": username, "email": email, "password": password}
    listUsers.append(new_user)
    return new_user


@app.post("/api/signup", response_model=DefaultResponse, tags=["auth"])
async def api_signup(user: UserSignUp):
    if await get_user_by_username(username=user.username):
        detail = {"result": False, "message": "Ошибка, это имя уже занято!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    if await get_user_by_email(email=user.email):
        detail = {"result": False, "message": "Ошибка, эта почта уже занята!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    await create_new_user(username=user.username, email=user.email, password=hash_password(user.password))

    return {"result": True, "message": "Вы успешно зарегистрировались!", "data": {}}


@app.get('/api/logout', response_model=DefaultResponse, tags=["auth"])
async def api_logout(response: Response, request: Request):
    access_token = request.cookies.get("user_token")

    if not access_token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    response.delete_cookie(key="user_token")

    return {"result": True, "message": "Выход выполнен успешно!", "data": {}}


@app.get('/api/home', response_model=DefaultResponse, tags=["auth"])
async def api_home(request: Request):
    access_token = request.cookies.get("user_token")

    if not access_token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    return {"result": True, "message": f"Добро пожаловать!", "data": {}}


# async def get_current_user(token=Cookie()):
#     if token is not None:
#         user = await get_user_by_token(token=token)
#         if user:
#             return user
#     detail = {"result": False, "message": "Неавторизованный пользователь!", "data": {}}
#     raise HTTPException(status_code=401, detail=detail)
#
#
# async def get_user_by_token(token: UUID4):
#     user = next((user for user in listToken if user["acces_token"] == token), None)
#     if user:
#         return user
#     else:
#         detail = {"result": False, "message": "Не верный токен!", "data": {}}
#         raise HTTPException(status_code=401, detail=detail)


@app.get("/api/products", tags=["products"])
async def read_products(request: Request):
    access_token = request.cookies.get("user_token")

    if not access_token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = next((token for token in listToken if token["access_token"] == access_token), None)
    if check_token:
        content = {"result": True, "message": "Успешно, список товаров был просмотрен!",
                   "data": sorted(listProducts, key=lambda x: x["product_id"])}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


async def get_product_by_id(product_id: int) -> dict:
    for product in listProducts:
        if product["product_id"] == product_id:
            return product


@app.get("/api/products/{product_id}", tags=["products"])
async def read_product(product_id: int, request: Request):
    token = request.cookies.get("user_token")

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    product = await get_product_by_id(product_id=product_id)
    if product is None:
        detail = {"result": False, "message": "Ошибка, товар с таким идентификатором не найден!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)

    content = {"result": True, "message": "Успешно, товар был просмотрен!", "data": product}
    return JSONResponse(content=content)


@app.post("/api/products", tags=["products"])
async def create_product(product: ProductSchema, request: Request):
    token = request.cookies.get("user_token")

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    if any(j["product_id"] == product.product_id for j in listProducts):
        detail = {"result": False, "message": "Ошибка, товар с таким идентификатором уже существует!", "data": {}}
        raise HTTPException(status_code=400, detail=detail)

    listProducts.append(product.dict())
    content = {"result": True, "message": f"Вы успешно добавили товар - {product.name_product.lower()}!",
               "data": product.name_product}
    return JSONResponse(content=content)


@app.get("/api/cart", tags=["cart"])
async def read_cart(request: Request):
    token = request.cookies.get("user_token")

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    content = {"result": True, "message": "Просмотр корзины совершенно успешно!",
               "data": sorted(listOfProductInCart, key=lambda x: x["product_id"])}
    return JSONResponse(content=content)


@app.post("/api/cart/{product_id}", tags=["cart"])
async def create_product_to_cart_by_id(product_id: int, request: Request):
    token = request.cookies.get("user_token")

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    product = await get_product_by_id(product_id=product_id)
    cart = CartSchema(product_id=product["product_id"], name_product=product["name_product"])
    listOfProductInCart.append(cart.dict())

    content = {"result": True,
               "message": f'Вы успешно добавили товар - {product.get("name_product").lower()} в корзину!',
               "data": product["name_product"]}
    return JSONResponse(content=content)


@app.post("/api/cart", tags=["cart"])
async def create_an_order_from_the_cart(request: Request):
    token = request.cookies.get("user_token")

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    data = [listOrder.append(i) for i in listOfProductInCart]
    listOfProductInCart.clear()
    content = {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
    return JSONResponse(content=content)


@app.get("/api/order", tags=["order"])
async def get_order(request: Request):
    token = request.cookies.get("user_token")

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    content = {"result": True, "message": "Заказ был успешно просмотрен!",
               "data": sorted(listOrder, key=lambda x: x['product_id'])}
    return JSONResponse(content=content)

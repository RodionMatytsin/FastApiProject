import hashlib
from pydantic import UUID4
from fastapi import FastAPI, HTTPException
from fastapi import Request, Cookie, Response, Depends
from starlette.responses import JSONResponse
from schemas import CreateProductSchema, UserLoginSchema, UserSignUp, DefaultResponse
from fake_db import listUsers, listToken, listProducts, listOrder, listOfProductInCart
from uuid import uuid4
from datetime import datetime, timedelta


app = FastAPI(title="Online service on FastAPI")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.get("/api/users", tags=["auth"])
async def read_users():
    data = sorted(listUsers, key=lambda x: x["user_id"])
    content = {"result": True, "message": "Успешно, список пользователей был просмотрен!", "data": data}
    return JSONResponse(content=content)


@app.get("/api/users_token", tags=["auth"])
async def read_users_token():
    data = [
        {
            "user_id": token["user_id"],
            "access_token": token["access_token"],
            "expire": token["expire"].isoformat(),
            "datetime_create": token["datetime_create"].isoformat()
        }
        for token in sorted(listToken, key=lambda x: x["user_id"])
    ]

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
        new_token = {
            "user_id": user_id,
            "access_token": str(uuid4()),
            "expire": datetime.utcnow() + timedelta(weeks=1),
            "datetime_create": datetime.utcnow()
        }
        listToken.append(new_token)
        return new_token
    else:
        if datetime.utcnow() > check_token["expire"]:
            check_token["access_token"] = str(uuid4())
            check_token["expire"] = datetime.utcnow() + timedelta(weeks=1)
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
    return next((user for user in listUsers if user["username"] == username), None)


async def get_user_by_email(email: str) -> dict:
    return next((user for user in listUsers if user["email"] == email), None)


async def create_new_user(username: str, email: str, password: str) -> dict:
    if await get_user_by_username(username=username):
        detail = {"result": False, "message": "Ошибка, это имя уже занято!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    if await get_user_by_email(email=email):
        detail = {"result": False, "message": "Ошибка, эта почта уже занята!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    last_user_id = max([user["user_id"] for user in listUsers]) + 1 if listUsers else 0
    new_user = {"user_id": last_user_id, "username": username, "email": email, "password": password}
    listUsers.append(new_user)
    return new_user


@app.post("/api/signup", response_model=DefaultResponse, tags=["auth"])
async def api_signup(user: UserSignUp):
    await create_new_user(username=user.username, email=user.email, password=hash_password(user.password))

    return {"result": True, "message": "Вы успешно зарегистрировались!", "data": {}}


async def get_user_token(request: Request) -> str:
    return request.cookies.get("user_token")


@app.get('/api/logout', response_model=DefaultResponse, tags=["auth"])
async def api_logout(response: Response, request: Request):
    token = await get_user_token(request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    response.delete_cookie(key="user_token")

    return {"result": True, "message": "Выход выполнен успешно!", "data": {}}


@app.get('/api/home', response_model=DefaultResponse, tags=["auth"])
async def api_home(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        return {"result": True, "message": "Добро пожаловать!", "data": {}}
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


async def get_check_token(access_token: str) -> str:
    return next((token for token in listToken
                 if token["access_token"] == access_token and token["expire"] > datetime.utcnow()), None)


@app.get("/api/products", tags=["products"])
async def read_products(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        content = {"result": True, "message": "Успешно, список товаров был просмотрен!",
                   "data": sorted(listProducts, key=lambda x: x["product_id"])}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


async def create_new_product(product: str) -> dict:
    last_product_id = max([product["product_id"] for product in listProducts]) + 1 if listUsers else 0
    new_product = {"product_id": last_product_id, "name_product": product}
    listProducts.append(new_product)
    return new_product


@app.post("/api/products", tags=["products"])
async def create_product(product: CreateProductSchema, request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        await create_new_product(product=product.name_product)
        content = {"result": True, "message": f"Вы успешно добавили товар - {product.name_product.lower()}!",
                   "data": product.name_product}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


async def get_product_by_id(product_id: int) -> dict:
    return next((product for product in listProducts if product["product_id"] == product_id), None)


@app.get("/api/products/{product_id}", tags=["products"])
async def read_product(product_id: int, request: Request):
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

        content = {"result": True, "message": "Успешно, товар был просмотрен!", "data": product}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


async def get_user_token_by_id(access_token: str) -> int:
    return next((token["user_id"] for token in listToken if token["access_token"] == access_token), None)


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


async def add_product_to_cart(product_id: int, name_product: str, user_id: int) -> dict:
    new_product_in_cart = {"product_id": product_id, "name_product": name_product, "user_id": user_id}
    listOfProductInCart.append(new_product_in_cart)
    return new_product_in_cart


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


@app.get("/api/order", tags=["order"])
async def get_order(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        user_id = await get_user_token_by_id(access_token=token)
        data = [
            {
                "product_id": order["product_id"],
                "name_product": order["name_product"],
                "user_id": order["user_id"]
            }
            for order in sorted(listOrder, key=lambda x: x["product_id"])
            if order["user_id"] == user_id
        ]

        content = {"result": True, "message": "Заказ был успешно просмотрен!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

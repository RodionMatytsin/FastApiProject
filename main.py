from fastapi import FastAPI, HTTPException
from fastapi import Request, Cookie, Response
from starlette.responses import JSONResponse
from schemas import ProductSchema, CartSchema, UserLoginSchema, DefaultResponse, UserSignUp
import fake_db as db
from user_token import UserToken


app = FastAPI()


@app.get("/api/users", tags=["auth"])
async def read_users():
    content = {"result": True, "message": "Успешно, список пользователей был просмотрен!",
               "data": sorted(db.listUsers, key=lambda x: x["user_id"])}
    return JSONResponse(content=content)


@app.get("/api/users_token", tags=["auth"])
async def read_users_token():
    data = [{"user_id": user_token["user_id"],
             "acces_token": user_token["acces_token"],
             "expire": user_token["expire"].isoformat()}
            for user_token in sorted(db.listToken, key=lambda x: x["user_id"])]

    content = {"result": True, "message": "Успешно, список токенов был просмотрен!", "data": data}
    return JSONResponse(content=content)


async def get_current_user(username: str, password: str):
    for user in db.listUsers:
        if user["username"] == username and user["password"] == password:
            return user
    detail = {"result": False, "message": "Ошибка, неверный логин или пароль!", "data": {}}
    raise HTTPException(status_code=404, detail=detail)


@app.post("/api/login", response_model=DefaultResponse, tags=["auth"])
async def login_user(user: UserLoginSchema, request: Request, response: Response):
    user = await get_current_user(username=user.username, password=user.password)

    access_token = request.cookies.get("user_token")

    if not access_token or not UserToken(user_id=user["user_id"]).is_valid():
        user_token = UserToken(user_id=user["user_id"])
        db.listToken.append({
            "user_id": user["user_id"],
            "acces_token": user_token.access_token,
            "expire": user_token.expire
        })
        response.set_cookie(key="user_token", value=user_token.access_token, httponly=True)
    else:
        user_token = next((ut for ut in db.listToken if ut["acces_token"] == access_token), None)
        user_token["expire"] = UserToken(user_id=user["user_id"]).expire

    print(access_token)

    return {"result": True, "message": "Вы успешно авторизовались!", "data": {}}


async def get_user_by_username(username: str):
    for user in db.listUsers:
        if user["username"] == username:
            return user
    return None


async def get_user_by_email(email: str):
    for user in db.listUsers:
        if user["email"] == email:
            return user
    return None


async def create_new_user(username: str, email: str, password: str):
    last_user_id = max([user["user_id"] for user in db.listUsers]) + 1 if db.listUsers else 0
    new_user = {"user_id": last_user_id, "username": username, "email": email, "password": password}
    db.listUsers.append(new_user)
    return new_user


@app.post("/api/signup", response_model=DefaultResponse, tags=["auth"])
async def api_signup(user: UserSignUp, response: Response):
    if await get_user_by_username(username=user.username):
        detail = {"result": False, "message": "Ошибка, это имя уже занято!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    if await get_user_by_email(email=user.email):
        detail = {"result": False, "message": "Ошибка, эта почта уже занята!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    new_user = await create_new_user(username=user.username, email=user.email, password=user.password)
    user_token = UserToken(user_id=new_user["user_id"])
    db.listToken.append(
        {"user_id": new_user["user_id"],
         "acces_token": user_token.access_token,
         "expire": user_token.expire}
    )
    response.set_cookie(key="user_token", value=user_token.access_token, httponly=True)

    return {"result": True, "message": "Вы успешно зарегистрировались!", "data": {}}


@app.get('/api/logout', response_model=DefaultResponse, tags=["auth"])
async def logout(response: Response):
    response.delete_cookie(key="user_token")
    print(response.__dict__)
    return {"result": True, "message": "Выход выполнен успешно!", "data": {}}


@app.get('/api/home', response_model=DefaultResponse, tags=["auth"])
async def home(request: Request):
    access_token = request.cookies.get("user_token")
    if not access_token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    print(access_token)

    return {"result": True, "message": f"Добро пожаловать!", "data": {}}


@app.get("/api/products", tags=["products"])
async def read_products(request: Request):
    try:
        token = request.cookies.get("user_token")

        if not token:
            detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        content = {"result": True, "message": "Успешно, список товаров был просмотрен!",
                   "data": sorted(db.listProducts, key=lambda x: x["product_id"])}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при просмотре списка товаров: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


async def get_product_by_id(product_id: int):
    for product in db.listProducts:
        if product["product_id"] == product_id:
            return product
    return None


@app.get("/api/products/{product_id}", tags=["products"])
async def read_product(product_id: int, request: Request):
    try:
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
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при просмотре товара: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.post("/api/products", tags=["products"])
async def create_product(product: ProductSchema, request: Request):
    try:
        token = request.cookies.get("user_token")

        if not token:
            detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        if any(j["product_id"] == product.product_id for j in db.listProducts):
            detail = {"result": False, "message": "Ошибка, товар с таким идентификатором уже существует!", "data": {}}
            raise HTTPException(status_code=400, detail=detail)

        db.listProducts.append(product.dict())
        content = {"result": True, "message": f"Вы успешно добавили товар - {product.name_product.lower()}!",
                   "data": product.name_product}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при добавлении товара: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.get("/api/cart", tags=["cart"])
async def read_cart(request: Request):
    try:
        token = request.cookies.get("user_token")

        if not token:
            detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        content = {"result": True, "message": "Просмотр корзины совершенно успешно!",
                   "data": sorted(db.listOfProductInCart, key=lambda x: x["product_id"])}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка просмотра корзины: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.post("/api/cart/{product_id}", tags=["cart"])
async def create_product_to_cart_by_id(product_id: int, request: Request):
    try:
        token = request.cookies.get("user_token")

        if not token:
            detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        product = await get_product_by_id(product_id=product_id)
        cart = CartSchema(product_id=product["product_id"], name_product=product["name_product"])
        db.listOfProductInCart.append(cart.dict())

        content = {"result": True,
                   "message": f'Вы успешно добавили товар - {product.get("name_product").lower()} в корзину!',
                   "data": product["name_product"]}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка добавления товара в корзину: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.post("/api/cart", tags=["cart"])
async def create_an_order_from_the_cart(request: Request):
    try:
        token = request.cookies.get("user_token")

        if not token:
            detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        data = [db.listOrder.append(i) for i in db.listOfProductInCart]
        db.listOfProductInCart.clear()
        content = {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка оформления заказа в корзине: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.get("/api/order", tags=["order"])
async def get_order(request: Request):
    try:
        token = request.cookies.get("user_token")

        if not token:
            detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        content = {"result": True, "message": "Заказ был успешно просмотрен!",
                   "data": sorted(db.listOrder, key=lambda x: x['product_id'])}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при просмотре заказа: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)

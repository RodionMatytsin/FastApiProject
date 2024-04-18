from fastapi import FastAPI, HTTPException
from fastapi import Request, Cookie, Response
from starlette.responses import JSONResponse
from schemas import ProductSchema, CartSchema, UserLoginSchema, DefaultResponse
import fake_db as db
from UserToken import UserToken


app = FastAPI()


async def get_current_user(email, password):
    for user in db.listUsers:
        if user["email"] == email and user["password"] == password:
            return True
    detail = {"result": False, "message": "Ошибка, неверный логин или пароль!", "data": {}}
    raise HTTPException(status_code=404, detail=detail)


@app.post("/api/login", tags=["auth"])
async def login_user(user: UserLoginSchema, response: Response):
    valid_user = await get_current_user(user.email, user.password)

    if valid_user:
        user_token = UserToken(user.email)
        response.set_cookie(key='user_token', value=user_token.token, httponly=True, max_age=1209600)
        print(response.__dict__)
        content = {"result": True, "message": "Вы успешно авторизовались!", "data": {}}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Неверные учетные данные.", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


@app.get('/api/logout', response_model=DefaultResponse, tags=["auth"])
async def logout(response: Response):
    response.delete_cookie(key='user_token')
    print(response.__dict__)
    content = {"result": True, "message": "Выход выполнен успешно!", "data": {}}
    return JSONResponse(content=content)


@app.get('/api/home', tags=["auth"])
async def home(request: Request):
    token = request.cookies.get('user_token')
    print(token)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    try:
        user_token = UserToken(token)
    except ValueError:
        detail = {"result": False, "message": "Неверный токен!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    content = {"result": True, "message": "Добро пожаловать!", "data": user_token.token}
    return JSONResponse(content=content)


@app.get("/api/products", tags=["products"])
async def read_products(user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        content = {"result": True, "message": "Успешно, список товаров был просмотрен!",
                   "data": sorted(db.listProducts, key=lambda x: x['product_id'])}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при просмотре списка товаров: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.get("/api/products/{product_id}", tags=["products"])
async def read_product(product_id: int, user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        product = await get_product_by_id(product_id)
        if product is None:
            detail = {"result": False, "message": "Ошибка, товар с таким идентификатором не найден!", "data": {}}
            raise HTTPException(status_code=404, detail=detail)

        content = {"result": True, "message": "Успешно, товар был просмотрен!", "data": product}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при просмотре товара: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


async def get_product_by_id(product_id: int):
    for product in db.listProducts:
        if product["product_id"] == product_id:
            return product


@app.post("/api/products", tags=["products"])
async def create_product(product: ProductSchema, user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        if any(j['product_id'] == product.product_id for j in db.listProducts):
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
async def read_cart(user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        content = {"result": True, "message": "Просмотр корзины совершенно успешно!",
                   "data": sorted(db.listOfProductInCart, key=lambda x: x['product_id'])}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка просмотра корзины: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.post("/api/cart/{product_id}", tags=["cart"])
async def create_product_to_cart_by_id(product_id: int, user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        product = await get_product_by_id(product_id)
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
async def create_an_order_from_the_cart(user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        data = [db.listOrder.append(i) for i in db.listOfProductInCart]
        db.listOfProductInCart.clear()
        content = {"result": True, "message": "Заказ был успешно оформлен!", "data": data}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка оформления заказа в корзине: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)


@app.get("/api/order", tags=["order"])
async def get_order(user_token = Cookie()):
    try:
        if user_token.user_token != 'valid_token':
            detail = {"result": False, "message": "Пожалуйста, войдите в систему.", "data": {}}
            raise HTTPException(status_code=401, detail=detail)

        content = {"result": True, "message": "Заказ был успешно просмотрен!",
                   "data": sorted(db.listOrder, key=lambda x: x['product_id'])}
        return JSONResponse(content=content)
    except Exception as ex:
        detail = {"result": False, "message": f"Ошибка при просмотре заказа: {ex}!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)

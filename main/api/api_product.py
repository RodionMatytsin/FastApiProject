from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.schemas.product import CreateProductSchema
from main.utils.auth import get_user_token, get_check_token
from main.utils.product import get_products, create_new_product, get_product


@app.get("/api/products", tags=["products"])
async def read_products(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        data = await get_products()
        content = {"result": True, "message": "Успешно, список товаров был просмотрен!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


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


@app.get("/api/products/{product_id}", tags=["products"])
async def read_product(product_id: int, request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        data = await get_product(product_id=product_id)
        content = {"result": True, "message": "Успешно, товар был просмотрен!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

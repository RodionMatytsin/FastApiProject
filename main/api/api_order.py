from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.models.fake_db import listOrder
from main.utils.auth import get_user_token, get_check_token, get_user_token_by_id


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

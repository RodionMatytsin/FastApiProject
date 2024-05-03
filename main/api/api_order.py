from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.utils.auth import get_user_token, get_check_token
from main.utils.order import get_order


@app.get("/api/order", tags=["order"])
async def read_order(request: Request):
    token = await get_user_token(request=request)

    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

    check_token = await get_check_token(access_token=token)
    if check_token:
        data = await get_order(check_token=check_token)
        content = {"result": True, "message": "Заказ был успешно просмотрен!", "data": data}
        return JSONResponse(content=content)
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)

from main import app
from fastapi import HTTPException, Request
from main.utils.auth import authenticate_user, get_user_id
from main.utils.order import get_order


@app.get("/api/order", tags=["order"])
async def read_order(request: Request):
    await authenticate_user(request)
    data = await get_order(user_id=await get_user_id(request))
    return {"result": True, "message": "Заказ был успешно просмотрен!", "data": data}

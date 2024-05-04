from main import app
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from main.utils.auth import authenticate_user, get_user_id
from main.utils.order import get_order


@app.get("/api/order", tags=["order"])
async def read_order(request: Request):
    if await authenticate_user(request):
        data = await get_order(user_id=await get_user_id(request))
        content = {"result": True, "message": "Заказ был успешно просмотрен!", "data": data}
        return JSONResponse(content=content)

from main import app
from fastapi import Depends
from main.utils.order import get_order
from main.utils.auth import get_current_user
from main.schemas.response import DefaultResponse


@app.get("/api/order", status_code=200, tags=["Order"])
async def read_order(user=Depends(get_current_user)):
    return DefaultResponse(data=await get_order(user_id=user.id))

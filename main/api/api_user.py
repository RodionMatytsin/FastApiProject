from main import app
from main.utils.user import get_users, get_users_token
from starlette.responses import JSONResponse


@app.get("/api/users", tags=["user"])
async def read_users():
    data = await get_users()
    content = {"result": True, "message": "Успешно, список пользователей был просмотрен!", "data": data}
    return JSONResponse(content=content)


@app.get("/api/users_token", tags=["user"])
async def read_users_token():
    data = await get_users_token()
    content = {"result": True, "message": "Успешно, список токенов был просмотрен!", "data": data}
    return JSONResponse(content=content)

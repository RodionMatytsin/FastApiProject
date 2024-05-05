from main import app
from main.utils.auth import get_users, get_users_token


@app.get("/api/users", tags=["user"])
async def read_users():
    data = await get_users()
    return {"result": True, "message": "Успешно, список пользователей был просмотрен!", "data": data}


@app.get("/api/users_token", tags=["user"])
async def read_users_token():
    data = await get_users_token()
    return {"result": True, "message": "Успешно, список токенов был просмотрен!", "data": data}

from main import app
from main.models.fake_db import listUsers, listToken
from starlette.responses import JSONResponse


@app.get("/api/users", tags=["user"])
async def read_users():
    data = sorted(listUsers, key=lambda x: x["user_id"])
    content = {"result": True, "message": "Успешно, список пользователей был просмотрен!", "data": data}
    return JSONResponse(content=content)


@app.get("/api/users_token", tags=["user"])
async def read_users_token():
    data = [
        {
            "user_id": token["user_id"],
            "access_token": token["access_token"],
            "expire": token["expire"].isoformat(),
            "datetime_create": token["datetime_create"].isoformat()
        }
        for token in sorted(listToken, key=lambda x: x["user_id"])
    ]

    content = {"result": True, "message": "Успешно, список токенов был просмотрен!", "data": data}
    return JSONResponse(content=content)

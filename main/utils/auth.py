from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import Request
from main.models.fake_db import listUsers, listToken
from fastapi import HTTPException


async def get_user(username: str, password: str) -> dict:
    for user in listUsers:
        if user["username"] == username and user["password"] == password:
            return user
    detail = {"result": False, "message": "Ошибка, неверный логин или пароль!", "data": {}}
    raise HTTPException(status_code=404, detail=detail)


async def update_user_token(user_id: int) -> dict:
    check_token = next((token for token in listToken if token["user_id"] == user_id), None)
    if check_token is None:
        new_token = {
            "user_id": user_id,
            "access_token": str(uuid4()),
            "expire": datetime.utcnow() + timedelta(weeks=1),
            "datetime_create": datetime.utcnow()
        }
        listToken.append(new_token)
        return new_token
    else:
        if datetime.utcnow() > check_token["expire"]:
            check_token["access_token"] = str(uuid4())
            check_token["expire"] = datetime.utcnow() + timedelta(weeks=1)
            return check_token
        else:
            return check_token


async def get_user_by_username(username: str) -> dict:
    return next((user for user in listUsers if user["username"] == username), None)


async def get_user_by_email(email: str) -> dict:
    return next((user for user in listUsers if user["email"] == email), None)


async def create_new_user(username: str, email: str, password: str) -> dict:
    if await get_user_by_username(username=username):
        detail = {"result": False, "message": "Ошибка, это имя уже занято!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    if await get_user_by_email(email=email):
        detail = {"result": False, "message": "Ошибка, эта почта уже занята!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    last_user_id = max([user["user_id"] for user in listUsers]) + 1 if listUsers else 0
    new_user = {"user_id": last_user_id, "username": username, "email": email, "password": password}
    listUsers.append(new_user)
    return new_user


async def get_user_token(request: Request) -> str:
    return request.cookies.get("user_token")


async def get_check_token(access_token: str) -> str:
    return next((t for t in listToken if t["access_token"] == access_token and t["expire"] > datetime.utcnow()), None)


async def get_user_token_by_id(access_token: str) -> int:
    return next((token["user_id"] for token in listToken if token["access_token"] == access_token), None)

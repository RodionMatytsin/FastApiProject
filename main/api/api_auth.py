from main import app
from main.models.fake_db import hash_password
from fastapi import HTTPException, Response, Request
from main.schemas.response import ResponseDict
from main.schemas.user import UserSignUp, UserLoginSchema
from main.utils.auth import get_user, update_user_token, create_new_user, authenticate_user


@app.post("/api/login", response_model=ResponseDict, tags=["auth"])
async def api_login(user: UserLoginSchema, response: Response):
    user = await get_user(username=user.username, password=hash_password(user.password))
    user_token = await update_user_token(user_id=user["user_id"])
    response.set_cookie(key="user_token", value=user_token["access_token"], httponly=True)
    return {"result": True, "message": "Вы успешно авторизовались!", "data": {}}


@app.post("/api/signup", response_model=ResponseDict, tags=["auth"])
async def api_signup(user: UserSignUp):
    await create_new_user(username=user.username, email=user.email, password=hash_password(user.password))
    return {"result": True, "message": "Вы успешно зарегистрировались!", "data": {}}


@app.get('/api/logout', response_model=ResponseDict, tags=["auth"])
async def api_logout(response: Response, request: Request):
    await authenticate_user(request)
    response.delete_cookie(key="user_token")
    return {"result": True, "message": "Выход выполнен успешно!", "data": {}}


@app.get('/api/home', response_model=ResponseDict, tags=["auth"])
async def api_home(request: Request):
    await authenticate_user(request)
    return {"result": True, "message": "Добро пожаловать!", "data": {}}

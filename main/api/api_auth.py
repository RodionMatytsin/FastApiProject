from main import app
from main.models.database import hash_password
from fastapi import Response, Request
from main.schemas.response import ResponseDict
from main.schemas.user import UserSignUp, UserLoginSchema
# from main.utils.auth import get_user, update_user_token, create_new_user, authenticate_user
from main.utils.auth import get_u, update_u_t, create_new_u, auth_user


@app.post("/api/login", response_model=ResponseDict, tags=["auth"])
async def api_login(user: UserLoginSchema, response: Response):
    # user = await get_user(username=user.username, password=hash_password(user.password))
    # user_token = await update_user_token(user_id=user["user_id"])
    user = await get_u(username=user.username, password=hash_password(user.password))
    user_token = await update_u_t(user_id=user.id)
    response.set_cookie(key="user_token", value=user_token, httponly=True)
    return {"result": True, "message": "Вы успешно авторизовались!", "data": {}}


@app.post("/api/signup", response_model=ResponseDict, tags=["auth"])
async def api_signup(user: UserSignUp):
    # await create_new_user(username=user.username, password=hash_password(user.password), email=user.email)
    await create_new_u(username=user.username, password=hash_password(user.password), email=user.email)
    return {"result": True, "message": "Вы успешно зарегистрировались!", "data": {}}


@app.get('/api/logout', response_model=ResponseDict, tags=["auth"])
async def api_logout(response: Response, request: Request):
    await auth_user(request)
    response.delete_cookie(key="user_token")
    return {"result": True, "message": "Выход выполнен успешно!", "data": {}}


@app.get('/api/home', response_model=ResponseDict, tags=["auth"])
async def api_home(request: Request):
    await auth_user(request)
    return {"result": True, "message": "Добро пожаловать!", "data": {}}

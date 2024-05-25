from main import app
from fastapi import Depends
from main.schemas.response import DefaultResponse
from main.utils.auth import get_login_user, get_signup_user, get_logout_user, get_current_user


@app.post("/api/login", status_code=200, tags=["Auth"])
async def api_login_user(user=Depends(get_login_user)):
    return DefaultResponse(data=user)


@app.post("/api/signup", status_code=200, tags=["Auth"])
async def api_signup_user(user=Depends(get_signup_user)):
    return DefaultResponse(data=user)


@app.get('/api/logout', status_code=200, tags=["Auth"])
async def api_logout_user(response=Depends(get_logout_user)):
    return DefaultResponse(data=response)


@app.get('/api/home', status_code=200, tags=["Auth"])
async def api_home_user(user=Depends(get_current_user)):
    return DefaultResponse(data=user)

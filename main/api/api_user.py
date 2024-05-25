from main import app
from fastapi import Depends
from main.schemas.response import DefaultResponse
from main.utils.auth import get_users, get_tokens


@app.get("/api/users", status_code=200, tags=["Users"])
async def read_users(users=Depends(get_users)):
    return DefaultResponse(data=users)


@app.get("/api/tokens", status_code=200, tags=["Users"])
async def read_users_token(tokens=Depends(get_tokens)):
    return DefaultResponse(data=tokens)

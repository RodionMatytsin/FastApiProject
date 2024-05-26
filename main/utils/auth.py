from uuid import uuid4
from fastapi import HTTPException
from datetime import datetime
from main.schemas.user import UserRegular
from fastapi import Response, Cookie
from main.models.database import Users, Tokens
from main.models.database import hash_password
from main.schemas.user import UserSignUp, UserLoginSchema


async def get_user(username_: str, password_: str) -> UserRegular:
    user = await Users.get_user_(username_=username_, password_=password_)

    if not user:
        raise HTTPException(
            status_code=400,
            detail={"result": False, "message": "Ошибка, неверный логин или пароль!", "data": {}}
        )

    return UserRegular(
        id=user.id,
        username=user.username,
        email=user.email
    )


async def update_user_token(user_id_: int) -> str:
    check_token = await Tokens.get_user_token_(user_id_=user_id_)
    if not check_token:
        await Tokens.add_user_token_(user_id_=user_id_)
        get_new_token = await Tokens.get_user_token_(user_id_=user_id_)
        return get_new_token.access_token
    else:
        if datetime.now() > check_token.expires:
            new_token_ = str(uuid4())
            await Tokens.set_user_token_(new_token_=new_token_, user_id_=user_id_)
            return new_token_
        else:
            return check_token.access_token


async def get_login_user(user: UserLoginSchema, response: Response):
    user = await get_user(username_=user.username, password_=hash_password(user.password))
    token = await update_user_token(user_id_=user.id)
    response.set_cookie(key="user_token", value=token, httponly=True)
    return user


async def get_user_by_username(username_: str) -> UserRegular | None:
    user = await Users.get_user_by_username_(username_=username_)
    if user:
        return UserRegular(
            id=user.id,
            username=user.username,
            email=user.email
        )
    return None


async def get_user_by_email(email_: str) -> UserRegular | None:
    user = await Users.get_user_by_email_(email_=email_)
    if user:
        return UserRegular(
            id=user.id,
            username=user.username,
            email=user.email
        )
    return None


async def create_new_user(username_: str, password_: str, email_: str) -> UserRegular:
    if await get_user_by_username(username_=username_):
        raise HTTPException(
            status_code=409,
            detail={"result": False, "message": "Ошибка, данный логин уже занят!", "data": {}}
        )

    if await get_user_by_email(email_=email_):
        raise HTTPException(
            status_code=409,
            detail={"result": False, "message": "Ошибка, данная почта уже занята!", "data": {}}
        )

    await Users.add_user_(username_=username_, password_=password_, email_=email_)
    user = await Users.get_user_(username_=username_, password_=password_)

    return UserRegular(
        id=user.id,
        username=user.username,
        email=user.email
    )


async def get_signup_user(user: UserSignUp, response: Response) -> UserRegular:
    new_user = await create_new_user(username_=user.username, password_=hash_password(user.password), email_=user.email)
    token = await update_user_token(user_id_=new_user.id)
    response.set_cookie(key="user_token", value=token, httponly=True)
    return new_user


async def get_logout_user(response: Response):
    response.delete_cookie(key="user_token")


async def get_check_token(token_: str) -> object | None:
    check_token = await Tokens.get_check_token_(token_=token_)
    if check_token:
        return check_token
    return None


async def get_current_user(user_token=Cookie(default=None)) -> UserRegular:
    if user_token is None:
        raise HTTPException(
            status_code=401,
            detail={"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        )

    check_token = await get_check_token(token_=user_token)
    if check_token:
        user = await Users.get_user_by_user_id_(user_id_=check_token.user_id)
        return UserRegular(
            id=user.id,
            username=user.username,
            email=user.email
        )
    else:
        raise HTTPException(
            status_code=401,
            detail={"result": False, "message": "Ваш токен истек, войдите еще раз в систему!", "data": {}}
        )


async def get_users():
    data = await Users.get_users_()
    return [dict(id=row[0], username=row[1], password=row[2], email=row[3]) for row in data]


async def get_tokens():
    data = await Tokens.get_tokens_()
    return [dict(id=i[0], access_token=i[1], datetime_create=i[2], expires=i[3], user_id=i[4]) for i in data]

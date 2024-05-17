from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import Request
from main.schemas.user import UserRegular
from main.models.database import query_execute
from fastapi import HTTPException
from main.utils.another import escape


async def get_user(username: str, password: str) -> UserRegular:
    user = await query_execute(
        query_text=f'SELECT '
                   f'U.id, '
                   f'U.username, '
                   f'U.password, '
                   f'U.email '
                   f'FROM "Users" AS U '
                   f'WHERE U.username = \'{username}\' AND U.password = \'{password}\'',
        fetch_all=False,
        type_query='read'
    )

    if user is None:
        detail = {"result": False, "message": "Ошибка, неверный логин или пароль!", "data": {}}
        raise HTTPException(status_code=404, detail=detail)

    return UserRegular(
        id=user.id,
        username=user.username,
        password=user.password,
        email=user.email
    )


async def update_user_token(user_id: int):
    check_token = await query_execute(
        query_text=f'SELECT * FROM "Tokens" AS T WHERE T.user_id = {user_id}',
        fetch_all=False,
        type_query='read'
    )
    if check_token is None:
        await query_execute(
            query_text=f'INSERT INTO "Tokens" (access_token, datetime_create, expires, user_id) '
                       f'VALUES (\'{str(uuid4())}\', \'{datetime.now()}\', '
                       f'\'{datetime.now() + timedelta(weeks=1)}\', {user_id})',
            fetch_all=False,
            type_query='insert'
        )
        get_new_token = await query_execute(
            query_text=f'SELECT * FROM "Tokens" AS T WHERE T.user_id = {user_id}',
            fetch_all=False,
            type_query='read'
        )
        return get_new_token.access_token
    else:
        if datetime.now() > check_token.expires:
            new_token = str(uuid4())
            await query_execute(
                query_text=f'UPDATE "Tokens" AS T '
                           f'SET access_token = \'{new_token}\', expires = \'{datetime.now() + timedelta(weeks=1)}\' '
                           f'WHERE T.user_id = {user_id}',
                fetch_all=False,
                type_query='update'
            )
            return new_token
        else:
            return check_token.access_token


async def get_user_by_username(username: str) -> UserRegular | None:
    user = await query_execute(
        query_text=f'SELECT '
                   f'U.id, '
                   f'U.username, '
                   f'U.password, '
                   f'U.email '
                   f'FROM "Users" AS U '
                   f'WHERE U.username = \'{username}\'',
        fetch_all=False,
        type_query='read'
    )
    if user is not None:
        return UserRegular(
            id=user.id,
            username=user.username,
            password=user.password,
            email=user.email
        )
    return None


async def get_user_by_email(email: str) -> UserRegular | None:
    user = await query_execute(
        query_text=f'SELECT '
                   f'U.id, '
                   f'U.username, '
                   f'U.password, '
                   f'U.email '
                   f'FROM "Users" AS U '
                   f'WHERE U.email = \'{email}\'',
        fetch_all=False,
        type_query='read'
    )
    if user is not None:
        return UserRegular(
            id=user.id,
            username=user.username,
            password=user.password,
            email=user.email
        )
    return None


async def create_new_user(username: str, password: str, email: str):
    if await get_user_by_username(username=username):
        detail = {"result": False, "message": "Ошибка, это имя уже занято!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    if await get_user_by_email(email=email):
        detail = {"result": False, "message": "Ошибка, эта почта уже занята!", "data": {}}
        raise HTTPException(status_code=409, detail=detail)

    try:
        await query_execute(
            query_text=f'INSERT INTO "Users" (username, password, email) '
                       f'VALUES (\'{escape(username)}\', \'{password}\', \'{escape(email)}\')',
            fetch_all=False,
            type_query='insert'
        )
    except Exception as e:
        detail = {"result": False, "message": f"Произошла ошибка при создании пользователя - {e}.", "data": {}}
        raise HTTPException(status_code=500, detail=detail)


async def get_user_token(request: Request) -> str:
    return request.cookies.get("user_token")


async def get_check_token(access_token: str) -> int | None:
    user_id = await query_execute(
        query_text=f'SELECT '
                   f'T.id '
                   f'FROM "Tokens" AS T '
                   f'WHERE T.access_token = \'{access_token}\' AND T.expires > \'{datetime.now()}\'',
        fetch_all=False,
        type_query='read'
    )
    if user_id is not None:
        return user_id
    return None


async def authenticate_user(request: Request) -> bool:
    token = await get_user_token(request=request)
    if not token:
        detail = {"result": False, "message": "Пожалуйста, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)
    check_token = await get_check_token(access_token=token)
    if check_token:
        return True
    else:
        detail = {"result": False, "message": "Ваш токен истек, войдите в систему!", "data": {}}
        raise HTTPException(status_code=401, detail=detail)


async def get_user_id(request: Request) -> int:
    return await get_check_token(await get_user_token(request))


async def get_users():
    data = await query_execute(
        query_text=f'SELECT '
                   f'U.id, '
                   f'U.username, '
                   f'U.password, '
                   f'U.email '
                   f'FROM "Users" AS U '
                   f'ORDER BY U.id',
        fetch_all=True,
        type_query='read'
    )
    return [dict(id=row[0], username=row[1], password=row[2], email=row[3]) for row in data]


async def get_users_token():
    data = await query_execute(
        query_text=f'SELECT '
                   f'T.id, '
                   f'T.access_token, '
                   f'T.datetime_create, '
                   f'T.expires, '
                   f'T.user_id '
                   f'FROM "Tokens" AS T '
                   f'ORDER BY T.id',
        fetch_all=True,
        type_query='read'
    )
    return [dict(id=i[0], access_token=i[1], datetime_create=i[2], expires=i[3], user_id=i[4]) for i in data]

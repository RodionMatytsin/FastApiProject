from main.models.fake_db import listUsers, listToken


async def get_users() -> list:
    return sorted(listUsers, key=lambda x: x["user_id"])


async def get_users_token() -> list:
    data = [
        {
            "user_id": token["user_id"],
            "access_token": token["access_token"],
            "expire": token["expire"].isoformat(),
            "datetime_create": token["datetime_create"].isoformat()
        }
        for token in sorted(listToken, key=lambda x: x["user_id"])
    ]
    return data

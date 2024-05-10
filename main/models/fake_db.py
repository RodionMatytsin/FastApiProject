import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


listProducts = [
    {
        "product_id": 1,
        "name_product": "Мясо"
    },
    {
        "product_id": 3,
        "name_product": "Картофель"
    },
    {
        "product_id": 2,
        "name_product": "Молоко"
    },
{
        "product_id": 4,
        "name_product": "Рыба"
    },
{
        "product_id": 5,
        "name_product": "Бекон"
    },
{
        "product_id": 6,
        "name_product": "Йогурт"
    },
]

listOfProductInCart = []

listOrder = []

listToken = []

listUsers = [
    {
        "user_id": 1,
        "username": "aboba",
        "email": "123@mail.ru",
        "password": "c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646"
    },
    {
        "user_id": 2,
        "username": "admin",
        "email": "adm@mail.ru",
        "password": "ce3a598687c8d2e5aa6bedad20e059b4a78cca0adad7e563b07998d5cd226b8c"
    }
]

# 1234567890 - c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646
# 9999999999 - ce3a598687c8d2e5aa6bedad20e059b4a78cca0adad7e563b07998d5cd226b8c

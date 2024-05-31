from sqlalchemy import Column, DateTime, ForeignKey, Text, Boolean, String, BigInteger, SmallInteger, Time, Date
from sqlalchemy import func, select, update, insert, case, desc, delete, null, or_, and_, text, UUID
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs, AsyncSession
import main.config as config
from datetime import datetime, time, timedelta
from typing import Type
from uuid import uuid4
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False)

    @classmethod
    async def get_user_(cls, username_: str, password_: str) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.username, cls.password, cls.email],
                                                 join_=[],
                                                 where_=[cls.username == username_, cls.password == password_],
                                                 result_all=False)

    @classmethod
    async def get_user_by_email_(cls, email_: str) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.username, cls.password, cls.email],
                                                 join_=[],
                                                 where_=[cls.email == email_],
                                                 result_all=False)

    @classmethod
    async def get_user_by_username_(cls, username_: str) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.username, cls.password, cls.email],
                                                 join_=[],
                                                 where_=[cls.username == username_],
                                                 result_all=False)

    @classmethod
    async def get_user_by_user_id_(cls, user_id_: int) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.username, cls.password, cls.email],
                                                 join_=[],
                                                 where_=[cls.id == user_id_],
                                                 result_all=False)

    @classmethod
    async def get_users_(cls) -> list[object]:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.username, cls.password, cls.email],
                                                 join_=[],
                                                 where_=[],
                                                 result_all=True)

    @classmethod
    async def add_user_(cls, username_: str, password_: str, email_: str) -> None:
        values_ = {
            "username": username_,
            "password": password_,
            "email": email_
        }
        await DatabaseManager.add_result_(name_class_=Users, values_=values_)


class Tokens(Base):
    __tablename__ = 'tokens'
    id = Column(BigInteger, primary_key=True)
    access_token = Column(UUID(as_uuid=False), unique=True, nullable=False,
                          index=True, server_default=text('uuid_generate_v4()'))
    datetime_create = Column(DateTime, default=func.now(), nullable=False)
    expires = Column(DateTime, nullable=False)

    # Foreign Key
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)

    @classmethod
    async def get_user_token_(cls, user_id_: int) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.access_token, cls.datetime_create,
                                                          cls.expires, cls.user_id],
                                                 join_=[],
                                                 where_=[cls.user_id == user_id_],
                                                 result_all=False)

    @classmethod
    async def get_check_token_(cls, token_: str) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.access_token, cls.datetime_create,
                                                          cls.expires, cls.user_id],
                                                 join_=[],
                                                 where_=[cls.access_token == token_, cls.expires > datetime.now()],
                                                 result_all=False)

    @classmethod
    async def get_tokens_(cls) -> list[object]:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.access_token, cls.datetime_create,
                                                          cls.expires, cls.user_id],
                                                 join_=[],
                                                 where_=[],
                                                 result_all=True)

    @classmethod
    async def add_user_token_(cls, user_id_: int) -> None:
        values_ = {
            "access_token": uuid4(),
            "datetime_create": datetime.now(),
            "expires": datetime.now() + timedelta(weeks=1),
            "user_id": user_id_
        }
        await DatabaseManager.add_result_(name_class_=Tokens, values_=values_)

    @classmethod
    async def set_user_token_(cls, new_token_: str, user_id_: int) -> None:
        values_ = {
            "access_token": new_token_,
            "expires": datetime.now() + timedelta(weeks=1)
        }
        await DatabaseManager.update_result_(name_class_=Tokens, where_=[cls.user_id == user_id_], values_=values_)


class Products(Base):
    __tablename__ = 'products'
    id = Column(BigInteger, primary_key=True)
    name_product = Column(String(length=255), nullable=False)

    @classmethod
    async def get_products_(cls) -> list[object]:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.name_product],
                                                 join_=[],
                                                 where_=[],
                                                 result_all=True)

    @classmethod
    async def get_product_(cls, product_id: int) -> object:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.name_product],
                                                 join_=[],
                                                 where_=[cls.id == product_id],
                                                 result_all=False)

    @classmethod
    async def add_product_(cls, name_product_: str) -> None:
        await DatabaseManager.add_result_(name_class_=Products, values_={"name_product": name_product_})


class Carts(Base):
    __tablename__ = 'carts'
    id = Column(BigInteger, primary_key=True)

    # Foreign Key
    product_id = Column(BigInteger, ForeignKey(Products.id), nullable=False)
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)

    @classmethod
    async def get_cart_(cls, user_id: int) -> list[object]:
        return await DatabaseManager.get_result_(select_=[Products.name_product.label('name_product'), cls.user_id],
                                                 join_=[Products, Products.id == cls.product_id],
                                                 where_=[cls.user_id == user_id],
                                                 result_all=True)

    @classmethod
    async def get_all_cart_(cls, user_id: int) -> list[object]:
        return await DatabaseManager.get_result_(select_=[cls.id, cls.product_id, cls.user_id],
                                                 join_=[],
                                                 where_=[cls.user_id == user_id],
                                                 result_all=True)

    @classmethod
    async def add_cart_(cls, product_id_: int, user_id_: int) -> None:
        values_ = {
            "product_id": product_id_,
            "user_id": user_id_
        }
        await DatabaseManager.add_result_(name_class_=Carts, values_=values_)

    @classmethod
    async def delete_cart_(cls, user_id: int) -> None:
        await DatabaseManager.delete_result_(name_class_=Carts, where_=[cls.user_id == user_id])


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(BigInteger, primary_key=True)

    # Foreign Key
    cart_id = Column(BigInteger, ForeignKey(Carts.id), nullable=False)
    product_id = Column(BigInteger, ForeignKey(Products.id), nullable=False)
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)

    @classmethod
    async def get_order_(cls, user_id: int) -> list[object]:
        return await DatabaseManager.get_result_(select_=[Products.name_product.label('name_product'), cls.user_id],
                                                 join_=[Products, Products.id == cls.product_id],
                                                 where_=[cls.user_id == user_id],
                                                 result_all=True)

    @classmethod
    async def add_order_(cls, cart_id: int, product_id_: int, user_id_: int) -> None:
        values_ = {
            "cart_id": cart_id,
            "product_id": product_id_,
            "user_id": user_id_
        }
        await DatabaseManager.add_result_(name_class_=Orders, values_=values_)

    @classmethod
    async def delete_all_orders_for_cart_(cls, user_id: int) -> None:
        await DatabaseManager.delete_result_(name_class_=Orders, where_=[cls.user_id == user_id])


engine = create_async_engine(
        f'postgresql+asyncpg://{config.DATABASE_USER}'
        f':{config.DATABASE_PASSWORD}'
        f'@{config.DATABASE_IP}:{config.DATABASE_PORT}'
        f'/{config.DATABASE_NAME}',
        echo=False,
        pool_recycle=300,
        query_cache_size=0,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=2,
        pool_use_lifo=True
    )

# alembic init -t async main/alembic
# alembic revision --autogenerate -m "Init Alembic"
# alembic upgrade head

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class DatabaseManager:
    @asynccontextmanager
    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.commit()
                await session.close()

    @classmethod
    async def get_result_(
            cls,
            select_: list,
            join_: list = None,
            where_: list = list(),
            result_all: bool = False
    ) -> bool | object | list[object]:

        if not join_:
            query = select(*select_).where(*where_)
        else:
            query = select(*select_).join(*join_, isouter=True).where(*where_)

        async with cls.get_async_session() as session:
            result = await session.execute(query)
            result = result.all() if result_all else result.first()
        if result is None:
            return False
        return [x for x in result] if result_all else result

    @classmethod
    async def add_result_(cls, name_class_: object, values_: dict) -> None:
        async with cls.get_async_session() as session:
            await session.execute(insert(name_class_).values(**values_))

    @classmethod
    async def update_result_(cls, name_class_: object, where_: list, values_: dict) -> None:
        async with cls.get_async_session() as session:
            await session.execute(update(name_class_).where(*where_).values(**values_))

    @classmethod
    async def delete_result_(cls, name_class_: object, where_: list) -> None:
        async with cls.get_async_session() as session:
            await session.execute(delete(name_class_).where(*where_))

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
        return await Example.get_(select_=[cls.id, cls.username, cls.password, cls.email],
                                  where_=[cls.username == username_, cls.password == password_])

    @classmethod
    async def get_user_by_email_(cls, email_: str) -> object:
        return await Example.get_(select_=[cls.id, cls.username, cls.password, cls.email],
                                  where_=[cls.email == email_])

    @classmethod
    async def get_user_by_username_(cls, username_: str) -> object:
        return await Example.get_(select_=[cls.id, cls.username, cls.password, cls.email],
                                  where_=[cls.username == username_])

    @classmethod
    async def get_user_by_user_id_(cls, user_id_: int) -> object:
        return await Example.get_(select_=[cls.id, cls.username, cls.password, cls.email],
                                  where_=[cls.id == user_id_])

    @classmethod
    async def get_users_(cls) -> list[object]:
        return await Example.get_(select_=[cls.id, cls.username, cls.password, cls.email], type_=True)

    @classmethod
    async def add_user_(cls, username_: str, password_: str, email_: str) -> None:
        async with get_async_session() as session:
            await session.execute(insert(Users).values(
                username=username_,
                password=password_,
                email=email_
            ))


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
        return await Example.get_(select_=[cls.id, cls.access_token, cls.datetime_create, cls.expires, cls.user_id],
                                  where_=[cls.user_id == user_id_])

    @classmethod
    async def get_check_token_(cls, token_: str) -> object:
        return await Example.get_(select_=[cls.id, cls.access_token, cls.datetime_create, cls.expires, cls.user_id],
                                  where_=[cls.access_token == token_, cls.expires > datetime.now()])

    @classmethod
    async def get_tokens_(cls) -> list[object]:
        return await Example.get_(select_=[cls.id, cls.access_token, cls.datetime_create, cls.expires, cls.user_id],
                                  type_=True)

    @classmethod
    async def add_user_token_(cls, user_id_: int) -> None:
        async with get_async_session() as session:
            await session.execute(insert(Tokens).values(
                access_token=uuid4(),
                datetime_create=datetime.now(),
                expires=datetime.now() + timedelta(weeks=1),
                user_id=user_id_
            ))

    @classmethod
    async def set_user_token_(cls, new_token_: str, user_id_: int) -> None:
        async with get_async_session() as session:
            await session.execute(update(Tokens).where(cls.user_id == user_id_).values(
                access_token=new_token_, expires=datetime.now() + timedelta(weeks=1)
            ))


class Products(Base):
    __tablename__ = 'products'
    id = Column(BigInteger, primary_key=True)
    name_product = Column(String(length=255), nullable=False)

    @classmethod
    async def get_products_(cls) -> list[object]:
        return await Example.get_(select_=[cls.id, cls.name_product], type_=True)

    @classmethod
    async def get_product_(cls, product_id: int) -> object:
        return await Example.get_(select_=[cls.id, cls.name_product], where_=[cls.id == product_id])

    @classmethod
    async def add_product_(cls, name_product_: str) -> None:
        async with get_async_session() as session:
            await session.execute(insert(Products).values(name_product=name_product_))


class Carts(Base):
    __tablename__ = 'carts'
    id = Column(BigInteger, primary_key=True)

    # Foreign Key
    product_id = Column(BigInteger, ForeignKey(Products.id), nullable=False)
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)

    @classmethod
    async def get_cart_(cls, user_id: int) -> list[object]:
        return await Example.get_(select_=[Products.name_product.label('name_product'), cls.user_id],
                                  join_=[Products, Products.id == cls.product_id],
                                  where_=[cls.user_id == user_id], type_=True)

    @classmethod
    async def get_all_cart_(cls, user_id: int) -> list[object]:
        return await Example.get_(select_=[cls.id, cls.product_id, cls.user_id],
                                  where_=[cls.user_id == user_id], type_=True)

    @classmethod
    async def add_cart_(cls, product_id_: int, user_id_: int) -> None:
        async with get_async_session() as session:
            await session.execute(insert(Carts).values(product_id=product_id_, user_id=user_id_))

    @classmethod
    async def delete_cart_(cls, user_id: int):
        async with get_async_session() as session:
            await session.execute(delete(Carts).where(cls.user_id == user_id))


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(BigInteger, primary_key=True)

    # Foreign Key
    cart_id = Column(BigInteger, ForeignKey(Carts.id), nullable=False)
    product_id = Column(BigInteger, ForeignKey(Products.id), nullable=False)
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)

    @classmethod
    async def get_order_(cls, user_id: int) -> list[object]:
        return await Example.get_(select_=[Products.name_product.label('name_product'), cls.user_id],
                                  join_=[Products, Products.id == cls.product_id],
                                  where_=[cls.user_id == user_id], type_=True)

    @classmethod
    async def add_order_(cls, cart_id: int, product_id_: int, user_id_: int) -> None:
        async with get_async_session() as session:
            await session.execute(insert(Orders).values(cart_id=cart_id, product_id=product_id_, user_id=user_id_))

    @classmethod
    async def delete_all_orders_for_cart_(cls, user_id: int):
        async with get_async_session() as session:
            await session.execute(delete(Orders).where(cls.user_id == user_id))


class Example:
    @classmethod
    async def get_(cls, select_: list, join_: list = None, where_: list = None, type_: bool = False):
        kwargs = {
            "select_": select_,
            "join_": join_,
            "where_": where_,
            "type_": type_
        }
        return await Example.get_result_(kwargs=kwargs)

    @classmethod
    async def get_result_(cls, kwargs: dict):
        if not kwargs.get("join_"):
            query = select(*kwargs.get("select_")).where(and_(*kwargs.get("where_"))) \
                if kwargs.get("where_") else select(*kwargs.get("select_"))
        else:
            query = select(*kwargs.get("select_")).join(*kwargs.get("join_"), isouter=True).where(and_(*kwargs.get("where_"))) \
                if kwargs.get("where_") else select(*kwargs.get("select_")).join(*kwargs.get("join_"), isouter=True)

        async with get_async_session() as session:
            result = await session.execute(query)
            result = result.all() if kwargs.get("type_") else result.first()
        if result is None:
            return False
        return [x for x in result] if kwargs.get("type_") else result


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


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.commit()
            await session.close()

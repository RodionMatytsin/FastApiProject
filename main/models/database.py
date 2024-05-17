from sqlalchemy import Column, BigInteger, String, DateTime, UUID, ForeignKey
from sqlalchemy import func, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from main.config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_IP, DATABASE_PORT, DATABASE_NAME
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'Users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(length=40), nullable=False)
    password = Column(String(length=70), nullable=False)
    email = Column(String(length=90), nullable=False)


class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(BigInteger, primary_key=True)
    access_token = Column(UUID(as_uuid=False), unique=True, nullable=False,
                          index=True, server_default=text('uuid_generate_v4()'))
    datetime_create = Column(DateTime, default=func.now(), nullable=False)
    expires = Column(DateTime, nullable=False)

    # Foreign Key
    user_id = Column(BigInteger, ForeignKey(f'{Users.id}'), nullable=False)


class Products(Base):
    __tablename__ = 'Products'
    id = Column(BigInteger, primary_key=True)
    name_product = Column(String(length=100), nullable=False)


class Carts(Base):
    __tablename__ = 'Carts'
    id = Column(BigInteger, primary_key=True)

    # Foreign Key
    product_id = Column(BigInteger, ForeignKey(f'{Products.id}'), nullable=False)
    user_id = Column(BigInteger, ForeignKey(f'{Users.id}'), nullable=False)


class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(BigInteger, primary_key=True)

    # Foreign Key
    cart_id = Column(BigInteger, ForeignKey(f'{Carts.id}'), nullable=False)
    product_id = Column(BigInteger, ForeignKey(f'{Products.id}'), nullable=False)
    user_id = Column(BigInteger, ForeignKey(f'{Users.id}'), nullable=False)


engine = create_async_engine(
        f'postgresql+asyncpg://{DATABASE_USER}'
        f':{DATABASE_PASSWORD}'
        f'@{DATABASE_IP}:{DATABASE_PORT}'
        f'/{DATABASE_NAME}',
        echo=False,
        pool_recycle=300,
        query_cache_size=0,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=2,
        pool_use_lifo=True
    )

Session = async_sessionmaker(engine, expire_on_commit=False)


# alembic init -t async main/alembic
# alembic revision --autogenerate -m "Database creation"
# alembic upgrade 163541a49932


async def query_execute(query_text: str, fetch_all: bool = False, type_query: str = 'read'):
    async with Session() as db:
        print(query_text, fetch_all, type_query)
        query_object = await db.execute(text(query_text))
        if type_query == 'read':
            return query_object.fetchall() if fetch_all else query_object.fetchone()
        else:
            await db.execute(text('commit'))
            return True

from pydantic import BaseModel, EmailStr, Field
from fastapi import Cookie

class ProductSchema(BaseModel):
    product_id: int = Field()
    name_product: str = Field()


class CartSchema(BaseModel):
    product_id: int = Field()
    name_product: str = Field()


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field()


class UserSignUp(BaseModel):
    email: EmailStr
    password: str = Field()


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict
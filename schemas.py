from pydantic import BaseModel, EmailStr, Field


class ProductSchema(BaseModel):
    product_id: int = Field()
    name_product: str = Field()


class CartSchema(BaseModel):
    product_id: int = Field()
    name_product: str = Field()


class UserLoginSchema(BaseModel):
    username: str = Field()
    password: str = Field()


class UserSignUp(BaseModel):
    username: str = Field()
    email: EmailStr
    password: str = Field()


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict
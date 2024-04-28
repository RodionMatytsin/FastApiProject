from pydantic import BaseModel, EmailStr, Field


class ProductSchema(BaseModel):
    product_id: int = Field()
    name_product: str = Field()


class CartSchema(BaseModel):
    product_id: int = Field()
    name_product: str = Field()


class UserLoginSchema(BaseModel):
    username: str = Field(pattern=r'^([a-zA-Z0-9_-|\\\/?.()*%$#@!<>{}\[\]]){5,25}$')
    password: str = Field(pattern=r'^([a-zA-Z0-9_]|\W){8,64}$')


class UserSignUp(BaseModel):
    username: str = Field(pattern=r'^([a-zA-Z0-9_-|\\\/?.()*%$#@!<>{}\[\]]){5,25}$')
    email: EmailStr
    password: str = Field(pattern=r'^([a-zA-Z0-9_]|\W){8,64}$')


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict

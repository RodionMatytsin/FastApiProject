from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    product_id: int = Field(default=None)
    name_product: str = Field(default=None)


class CartSchema(BaseModel):
    product_id: int = Field(default=None)
    name_product: str = Field(default=None)


class UserLoginSchema(BaseModel):
    email: str = Field(default=None)
    password: str = Field(default=None)


class DefaultResponse(BaseModel):
    result: bool
    message: str
    data: dict

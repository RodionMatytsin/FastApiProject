from pydantic import BaseModel, EmailStr, Field


class UserLoginSchema(BaseModel):
    username: str = Field(pattern=r'^([a-zA-Z0-9_-|\\\/?.()*%$#@!<>{}\[\]]){5,25}$')
    password: str = Field(pattern=r'^([a-zA-Z0-9_]|\W){8,64}$')


class UserSignUp(BaseModel):
    username: str = Field(pattern=r'^([a-zA-Z0-9_-|\\\/?.()*%$#@!<>{}\[\]]){5,25}$')
    email: EmailStr
    password: str = Field(pattern=r'^([a-zA-Z0-9_]|\W){8,64}$')


class UserRegular(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr

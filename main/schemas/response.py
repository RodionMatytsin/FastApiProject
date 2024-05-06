from pydantic import BaseModel


class DefaultResponseDict(BaseModel):
    result: bool
    message: str
    data: dict


class DefaultResponseList(BaseModel):
    result: bool
    message: str
    data: list

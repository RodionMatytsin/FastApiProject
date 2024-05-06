from pydantic import BaseModel


class BaseResponse(BaseModel):
    result: bool
    message: str


class ResponseDict(BaseResponse):
    data: dict


class ResponseList(BaseResponse):
    data: list

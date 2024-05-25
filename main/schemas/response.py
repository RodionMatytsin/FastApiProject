from pydantic import BaseModel


class DefaultResponse(BaseModel):
    result: bool = True
    message: str = 'Успех!'
    data: object | dict | list = {}

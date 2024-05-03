from pydantic import BaseModel, Field


class CreateProductSchema(BaseModel):
    name_product: str = Field()

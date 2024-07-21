from pydantic import BaseModel, Field, field_validator


class FuncAttributes(BaseModel):
    methods: list[str] = Field(
        ..., title='methods', description='The HTTP methods for the endpoint.'
    )
    url: str = Field(..., title='url', description='The URL path for the endpoint.')

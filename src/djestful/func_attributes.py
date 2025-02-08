from pydantic import BaseModel, Field

from djestful.types import HttpMethod


class FuncAttributes(BaseModel):
    methods: list[HttpMethod] = Field(
        ..., title='methods', description='The HTTP methods for the endpoint.'
    )
    path: str = Field(..., title='url', description='The URL path for the endpoint.')
    url_name: str | None = Field(
        None, title='url_name', description='The name of the URL pattern for the endpoint.'
    )

from djestful.types import DictStrAny
from pydantic import BaseModel


class Contact(BaseModel):
    name: str | None = None
    url: str | None = None
    email: str | None = None


class License(BaseModel):
    name: str
    identifier: str | None = None
    url: str | None = None


class Info(BaseModel):
    title: str
    description: str | None = None
    termsOfService: str | None = None
    contact: DictStrAny | None = None
    license: DictStrAny | None = None
    version: str


class ServerVariable(BaseModel):
    default: str
    enum: list[str] | None = None
    description: str | None = None


class Server(BaseModel):
    url: str
    description: str | None = None
    variables: dict[str, ServerVariable] | None = None


class OpenAPI(BaseModel):
    openapi: str = '3.0.1'
    info: Info
    jsonSchemaDialect: str | None = None
    servers: list[Server] | None = None

    # # Using Any for Specification Extensions
    # paths: Optional[Dict[str, Union[PathItem, Any]]] = None
    # webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
    # components: Optional[Components] = None
    # security: Optional[List[Dict[str, List[str]]]] = None
    # tags: Optional[List[Tag]] = None
    # externalDocs: Optional[ExternalDocumentation] = None

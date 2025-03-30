from django.conf import settings as django_global_settings
from django.utils.module_loading import import_string
from pydantic import BaseModel, Field, field_validator

from .openapi.schemas import DefaultOpenAPISchema


def get_default_schemas() -> dict[str, str]:
    """
    Returns the default OpenAPI schema.
    """
    return {
        'default': 'djestful.openapi.schemas.DefaultOpenAPISchema',
    }


class DjestfulSettings(BaseModel):
    OPENAPI_SCHEMAS: dict[str, str] = Field(
        description='OpenAPI schemas from modules',
        examples=[{'default': 'myapp.openapi.DefaultOpenAPISchema'}],
        default_factory=get_default_schemas,
    )

    @field_validator('OPENAPI_SCHEMAS')
    @classmethod
    def validate_schemas(clas, value: dict[str, str]) -> dict[str, str]:
        """
        Validates the schemas to ensure they are of type OpenAPI.
        """
        if 'default' not in value:
            raise ValueError('"default" schema is required in SCHEMAS')
        url_docs_list: list[str] = []
        url_openapi_json_list: list[str] = []
        for key, schema in value.items():
            try:
                schema_class = import_string(schema)
                if not issubclass(schema_class, DefaultOpenAPISchema):
                    raise ValueError(
                        f'Invalid schema "{key}": must be subclass of DefaultOpenAPISchema'
                        'You can use `djestful.openapi.schemas.DefaultOpenAPISchema`'
                        ' as a base class.'
                    )

                if schema_class.openapi_json_url in url_openapi_json_list:
                    raise ValueError(
                        f'`{key}` schema has the same openapi_json_url as another schema, '
                        f'please use different openapi_json_url: {schema_class.openapi_json_url}'
                    )
                if schema_class.docs_url in url_docs_list:
                    raise ValueError(
                        f'`{key}` schema has the same docs_url as another schema, '
                        f'please use different docs_url: {schema_class.docs_url}'
                    )
                url_docs_list.append(schema_class.docs_url)
                url_openapi_json_list.append(schema_class.openapi_json_url)

            except ImportError as e:
                raise ValueError(f'Invalid schema "{key}": {e}') from e

        return value


settings = DjestfulSettings(**getattr(django_global_settings, 'DJESTFUL_FRAMEWORK', {}))

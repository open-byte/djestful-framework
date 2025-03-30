from djestful.openapi.schemas import DefaultOpenAPISchema as Schema


class DefaultOpenAPISchema(Schema):
    title = 'Djestful API General'
    description = """This is a sample Pet Store Server based on the OpenAPI 3.0 specification.  You can find out more about\r\nSwagger at [https://swagger.io](https://swagger.io). In the third iteration of the pet store, we've switched to the design first approach!\r\nYou can now help us improve the API whether it's by making changes to the definition itself or to the code.\r\nThat way, with time, we can improve the API in general, and expose some of the new features in OAS3.\r\nSome useful links:\r\n- [The Pet Store repository](https://github.com/swagger-api/swagger-petstore)\r\n- [The source API definition for the Pet Store](https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml)"""  # noqa
    termsOfService = 'https://example.com/terms'
    version = '1.0.1'
    contact = {
        'name': 'Person Name',
        'url': 'https://example.com',
        'email': 'test@test.com',
    }
    license = {
        'name': 'MIT',
        'identifier': 'MIT',
        'url': 'https://example.com/license',
    }
    servers = [
        {
            'url': 'https://dev.djestful.com/api/v1',
            'description': 'Development server',
            'variables': {
                'port': {
                    'default': '8000',
                    'enum': ['8000', '8080'],
                    'description': 'The port for the API',
                }
            },
        },
        {
            'url': 'https://staging.djestful.com/api/v1',
            'description': 'Staging server',
        },
        {
            'url': 'https://prod.djestful.com/api/v1',
            'description': 'Production server',
        },
    ]


class InternalOpenAPISchema(Schema):
    title = 'Djestful API Internal'
    description = 'Internal API documentation'
    termsOfService = 'https://example.com/terms'
    version = '1.0.2'
    contact = {
        'name': 'Person Name Internal',
        'url': 'https://example.com/internal',
        'email': 'test@internal.com',
    }
    license = {
        'name': 'MIT Internal',
        'identifier': 'MIT Internal',
        'url': 'https://example.com/internal/license',
    }
    servers = [
        {
            'url': 'https://internal.djestful.com/api/v1',
            'description': 'Internal server',
            'variables': {
                'port': {
                    'default': '8000',
                    'enum': ['8000', '8080'],
                    'description': 'The port for the API',
                }
            },
        },
    ]

    docs_url = 'internal/docs/swagger/index.html'
    openapi_json_url = 'internal/docs/openapi.json'


class ExternalOpenAPISchema(Schema):
    title = 'Djestful API External'
    description = 'External API documentation'
    termsOfService = 'https://example.com/terms'
    version = '1.0.3'
    contact = {
        'name': 'Person Name External',
        'url': 'https://example.com/external',
        'email': 'test@external.com',
    }
    license = {
        'name': 'MIT External',
        'identifier': 'MIT External',
        'url': 'https://example.com/internal/license',
    }
    servers = [
        {
            'url': 'https://external.djestful.com/api/v1',
            'description': 'External server',
            'variables': {
                'port': {
                    'default': '8000',
                    'enum': ['8000', '8080'],
                    'description': 'The port for the API',
                }
            },
        },
    ]
    docs_url = 'external/docs/swagger/index.html'
    openapi_json_url = 'external/docs/openapi.json'

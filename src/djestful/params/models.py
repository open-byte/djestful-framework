from abc import ABC
from collections.abc import Callable
from typing import Any

from pydantic import AliasChoices, AliasPath, BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import deprecated


class ParamModel(BaseModel, ABC): ...


class QueryModel(ParamModel): ...


class PathModel(ParamModel): ...


class HeaderModel(ParamModel): ...


class CookieModel(ParamModel): ...


class BodyModel(ParamModel): ...


class FormModel(ParamModel): ...


class FileModel(ParamModel): ...


class Param(FieldInfo):
    _model: type[ParamModel] = ParamModel

    def __init__(
        self,
        default: Any,
        *,
        default_factory: Callable[[], Any] | None = None,
        annotation: Any | None = None,
        alias: str | None = None,
        alias_priority: int | None = None,
        # TODO: update when deprecating Pydantic v1, import these types
        # validation_alias: str | AliasPath | AliasChoices | None
        validation_alias: str | AliasPath | AliasChoices | None = None,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = None,
        multiple_of: float | None = None,
        allow_inf_nan: bool | None = None,
        max_digits: int | None = None,
        decimal_places: int | None = None,
        examples: list[Any] | None = None,
        openapi_examples: dict[str, Any] | None,  # dict[str, Example] | None = None,
        deprecated: deprecated | str | bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        self.include_in_schema = include_in_schema
        self.openapi_examples = openapi_examples
        kwargs = dict(
            default=default,
            default_factory=default_factory,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            discriminator=discriminator,
            multiple_of=multiple_of,
            allow_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **extra,
        )
        if examples is not None:
            kwargs['examples'] = examples

        current_json_schema_extra = json_schema_extra or extra
        kwargs['deprecated'] = deprecated

        kwargs.update(
            {
                'annotation': annotation,
                'alias_priority': alias_priority,
                'validation_alias': validation_alias,
                'serialization_alias': serialization_alias,
                'strict': strict,
                'json_schema_extra': current_json_schema_extra,
                'pattern': pattern,
            }
        )
        use_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        super().__init__(**use_kwargs)

    @classmethod
    def _param_source(cls) -> str:
        "Openapi param.in value or body type"
        return cls.__name__.lower()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.default})'


class Path(Param):
    _model = PathModel


class Query(Param):
    _model = QueryModel


class Header(Param):
    _model = HeaderModel


class Cookie(Param):
    _model = CookieModel


class Body(Param):
    _model = BodyModel


class Form(Param):
    _model = FormModel


class File(Param):
    _model = FileModel

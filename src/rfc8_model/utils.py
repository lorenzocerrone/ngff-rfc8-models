"""Pydantic helpers shared by the RFC-8 models."""

from __future__ import annotations

from typing import Any, Literal, get_args, get_origin

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

_CUSTOM_TAG = "__custom__"


class OpenTypeUnion:
    """Annotated marker: discriminate a union on ``type`` with an open fallback.

    Use as ``Annotated[A | B | Custom, OpenTypeUnion()]``. Members whose
    ``type`` field is a ``Literal`` are matched by those values; exactly one
    member must declare ``type`` as an unconstrained string and receives every
    other value. The alias stays a plain union for static type checkers.
    """

    def __get_pydantic_core_schema__(
        self, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        tags: dict[str, type[BaseModel]] = {}
        custom: type[BaseModel] | None = None
        for model in get_args(source):
            annotation = model.model_fields["type"].annotation
            if get_origin(annotation) is Literal:
                for value in get_args(annotation):
                    if value in tags:
                        raise TypeError(f"Duplicate discriminator value {value!r}")
                    tags[value] = model
            elif custom is None:
                custom = model
            else:
                raise TypeError("OpenTypeUnion allows one member with open 'type'")
        if custom is None:
            raise TypeError("OpenTypeUnion needs one member with open 'type'")

        def pick(value: Any) -> str:
            if isinstance(value, dict):
                t = value.get("type")
            else:
                t = getattr(value, "type", None)
            return t if t in tags else _CUSTOM_TAG

        choices: dict[str, CoreSchema] = {
            value: handler.generate_schema(model) for value, model in tags.items()
        }
        choices[_CUSTOM_TAG] = handler.generate_schema(custom)
        return core_schema.tagged_union_schema(choices, discriminator=pick)

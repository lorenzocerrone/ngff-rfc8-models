from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .models import Node


class OmeAttributes(BaseModel):
    version: Literal["0.9dev42"] = "0.9dev42"
    payload: Node  # flatten


class Attributes(BaseModel):
    ome: OmeAttributes


class ZarrJson(BaseModel):
    node_type: Literal["group", "array"] = "group"
    zarr_format: Literal[3] = 3
    attributes: Attributes

    @classmethod
    def with_ome(cls, node: Node) -> ZarrJson:
        return cls(attributes=Attributes(ome=OmeAttributes(payload=node)))

    @property
    def path(self) -> str:
        return ""


class StandaloneJson(BaseModel):
    ome: OmeAttributes

    @classmethod
    def with_ome(cls, node: Node) -> ZarrJson:
        return cls(ome=OmeAttributes(payload=node))

    @property
    def path(self) -> str:
        return ""

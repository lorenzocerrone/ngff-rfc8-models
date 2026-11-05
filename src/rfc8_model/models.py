from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator, StringConstraints

Name = Annotated[str, StringConstraints(pattern=".+")]
Id = Annotated[str, StringConstraints(pattern="[a-zA-Z0-9-_.]+")]


class Path(BaseModel):
    type: Literal["zarr", "json"]
    format: Literal["relative"]
    href: str


class CoordinateSystemAxis(BaseModel):
    type: Literal["array", "space", "time", "channel", "coordinate", "displacement"]
    id: Id
    name: Name | None = None
    unit: str | None  # SHOULD
    discrete: bool | None = None  # MAY
    long_name: Name | None = None  # MAY


class CoordinateSystem(BaseModel):
    id: Id
    name: Name | None = None
    axes: list[CoordinateSystemAxis]


class CoordinateTransformationReference(BaseModel):
    type: Literal["coordinate_system"] = "coordinate_system"
    ref: Id
    path: Path | None = None


class _CoordinateTransformation(BaseModel):
    name: Name | None = None
    input: CoordinateTransformationReference
    output: CoordinateTransformationReference


class IdentityCoordinateTransformation(_CoordinateTransformation):
    type: Literal["identity"] = "identity"


class ScaleCoordinateTransformation(_CoordinateTransformation):
    type: Literal["scale"] = "scale"
    scale: tuple[float, ...]


class TranslateCoordinateTransformation(_CoordinateTransformation):
    type: Literal["translate"] = "translate"
    scale: tuple[float, ...]


CoordinateTransformation = Annotated[
    IdentityCoordinateTransformation
    | ScaleCoordinateTransformation
    | TranslateCoordinateTransformation,
    Discriminator("type"),
]


class ScaleDownsamplingCoordinateTransformation(BaseModel):
    type: Literal["scale"] = "scale"
    scale: tuple[float, ...]


class TranslateDownsamplingCoordinateTransformation(BaseModel):
    type: Literal["translate"] = "translate"
    translate: tuple[float, ...]


class MultiscaleNodeItem(BaseModel):
    type: Literal["singlescale"] = "singlescale"  # ??
    id: Id | None = None
    name: Name | None = None
    downsamplingTransformations: (
        tuple[ScaleDownsamplingCoordinateTransformation]
        | tuple[
            ScaleDownsamplingCoordinateTransformation,
            TranslateDownsamplingCoordinateTransformation,
        ]
        | tuple[
            TranslateDownsamplingCoordinateTransformation,
            ScaleDownsamplingCoordinateTransformation,
        ]
    )


class MultiscaleNode(BaseModel):
    type: Literal["multiscale"] = "multiscale"
    id: Id | None = None
    name: Name | None = None
    coordinate_systems: tuple[CoordinateSystem, ...]
    coordinate_transformations: tuple[CoordinateTransformation, ...] | None = None
    nodes: tuple[MultiscaleNodeItem, ...]
    traits: tuple[Trait, ...] | None = None


class MultiscaleNodeReference(BaseModel):
    type: Literal["multiscale"] = "multiscale"
    id: Id
    name: Name | None = None
    path: Path
    traits: tuple[Trait, ...] | None = None


LeafNodeReference = Annotated[MultiscaleNodeReference, Discriminator("type")]


class CollectionNode(BaseModel):
    type: Literal["collection"] = "collection"
    id: Id
    name: Name | None = None
    nodes: tuple[CollectionNode | CollectionNodeReference | LeafNodeReference, ...]
    traits: tuple[Trait, ...] | None = None


class CollectionNodeReference(BaseModel):
    type: Literal["collection"] = "collection"
    id: Id
    name: Name | None = None
    path: Path
    traits: tuple[Trait, ...] | None = None


class SceneTrait(BaseModel):
    type: Literal["scene"] = "scene"
    coordinate_systems: tuple[CoordinateSystem, ...] | None = None
    coordinate_transformations: tuple[CoordinateTransformation, ...]


Trait = Annotated[SceneTrait, Discriminator("type")]

Node = Annotated[MultiscaleNode | CollectionNode, Discriminator("type")]
NodeReference = Annotated[
    MultiscaleNodeReference | CollectionNodeReference, Discriminator("type")
]

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator, StringConstraints

Name = Annotated[str, StringConstraints(pattern="^.+$")]
Id = Annotated[str, StringConstraints(pattern="^[a-zA-Z0-9-_.]+$")]
Type = Annotated[str, StringConstraints(pattern="^.+$")]

CustomPathFormat = Annotated[str, StringConstraints(pattern="^.+$")]
PathFormat = Literal["relative"] | CustomPathFormat


class _Path(BaseModel):
    format: PathFormat
    href: str


class ZarrPath(_Path):
    type: Literal["zarr"] = "zarr"


class JsonPath(_Path):
    type: Literal["json"] = "json"


class CustomPath(_Path):
    type: Type


Path = Annotated[ZarrPath | JsonPath | CustomPath, Discriminator("type")]


class _CoordinateSystemAxis(BaseModel):
    id: Id
    name: Name | None = None
    unit: str | None  # SHOULD
    discrete: bool | None = None  # MAY
    long_name: Name | None = None  # MAY


class ArrayCoordinateSystemAxis(BaseModel):
    type: Literal["array"]


class SpaceCoordinateSystemAxis(BaseModel):
    type: Literal["space"]


class TimeCoordinateSystemAxis(BaseModel):
    type: Literal["time"]


class ChannelCoordinateSystemAxis(BaseModel):
    type: Literal["channel"]


class CoordinateCoordinateSystemAxis(BaseModel):
    type: Literal["coordinate"]


class DisplacementCoordinateSystemAxis(BaseModel):
    type: Literal["displacement"]


class CustomCoordinateSystemAxis(_CoordinateSystemAxis):
    type: Type


CoordinateSystemAxis = Annotated[
    ArrayCoordinateSystemAxis
    | SpaceCoordinateSystemAxis
    | TimeCoordinateSystemAxis
    | ChannelCoordinateSystemAxis
    | CoordinateCoordinateSystemAxis
    | DisplacementCoordinateSystemAxis
    | CustomCoordinateSystemAxis,
    Discriminator("type"),
]


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


class CustomCoordinateTransformation(_CoordinateTransformation):
    type: Type


CoordinateTransformation = Annotated[
    IdentityCoordinateTransformation
    | ScaleCoordinateTransformation
    | TranslateCoordinateTransformation
    | CustomCoordinateTransformation,
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


class CustomLeafNode(BaseModel):
    type: Type
    id: Id
    name: Name | None = None
    traits: tuple[Trait, ...] | None = None


class CustomLeafNodeReference(BaseModel):
    type: Type
    id: Id
    name: Name | None = None
    path: Path
    traits: tuple[Trait, ...] | None = None


class SceneTrait(BaseModel):
    type: Literal["scene"] = "scene"
    coordinate_systems: tuple[CoordinateSystem, ...] | None = None
    coordinate_transformations: tuple[CoordinateTransformation, ...]


class CustomTrait(BaseModel):
    type: Type


Trait = Annotated[SceneTrait | CustomTrait, Discriminator("type")]

LeafNodeReference = Annotated[
    MultiscaleNodeReference | CustomLeafNodeReference, Discriminator("type")
]
Node = Annotated[
    MultiscaleNode | CollectionNode | CustomLeafNode, Discriminator("type")
]
NodeReference = Annotated[
    LeafNodeReference | CollectionNodeReference,
    Discriminator("type"),
]

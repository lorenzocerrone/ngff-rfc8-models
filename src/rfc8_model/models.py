from __future__ import annotations

from typing import Annotated, Literal

from pydantic import MISSING, BaseModel, StringConstraints

from .utils import OpenTypeUnion

Name = Annotated[str, StringConstraints(pattern="^.+$")]
Id = Annotated[str, StringConstraints(pattern="^[a-zA-Z0-9-_.]+$")]
Type = Annotated[str, StringConstraints(pattern="^.+$")]

CustomPathFormat = Annotated[str, StringConstraints(pattern="^.+$")]


class RelativePathReferenceLocator(BaseModel):
    type: Literal["relative"] = "relative"
    path: Annotated[str, StringConstraints(pattern="^.+$")]


class ZarrReferenceLocator(BaseModel):
    type: Literal["zarr"] = "zarr"
    path: str | MISSING = MISSING


class JsonReferenceLocator(BaseModel):
    type: Literal["json"] = "json"


class IdReferenceLocator(BaseModel):
    type: Literal["id"] = "id"
    id: Id


class CustomReferenceLocator(BaseModel):
    type: Type


ReferenceLocator = Annotated[
    RelativePathReferenceLocator
    | ZarrReferenceLocator
    | JsonReferenceLocator
    | IdReferenceLocator
    | CustomReferenceLocator,
    OpenTypeUnion(),
]

ReferenceLocatorPipeline = tuple[ReferenceLocator, ...]


class _CoordinateSystemAxis(BaseModel):
    id: Id
    name: Name | MISSING = MISSING
    unit: str | MISSING  # SHOULD
    discrete: bool | MISSING = MISSING  # MAY
    long_name: Name | MISSING = MISSING  # MAY


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
    OpenTypeUnion(),
]


class CoordinateSystem(BaseModel):
    id: Id
    name: Name | MISSING = MISSING
    axes: list[CoordinateSystemAxis]


class CoordinateTransformationReference(BaseModel):
    type: Literal["coordinate_system"] = "coordinate_system"
    ref: ReferenceLocatorPipeline


class _CoordinateTransformation(BaseModel):
    name: Name | MISSING = MISSING
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
    OpenTypeUnion(),
]


class ScaleDownsamplingCoordinateTransformation(BaseModel):
    type: Literal["scale"] = "scale"
    scale: tuple[float, ...]


class TranslateDownsamplingCoordinateTransformation(BaseModel):
    type: Literal["translate"] = "translate"
    translate: tuple[float, ...]


class MultiscaleNodeArray(BaseModel):
    type: Literal["singlescale"] = "singlescale"  # ??
    id: Id | MISSING = MISSING
    name: Name | MISSING = MISSING
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
    id: Id | MISSING = MISSING
    name: Name | MISSING = MISSING
    coordinate_systems: tuple[CoordinateSystem, ...]
    coordinate_transformations: tuple[CoordinateTransformation, ...] | MISSING = MISSING
    arrays: tuple[MultiscaleNodeArray, ...]
    traits: tuple[Trait, ...] | MISSING = MISSING


class MultiscaleNodeReference(BaseModel):
    type: Literal["multiscale"] = "multiscale"
    id: Id
    name: Name | MISSING = MISSING
    ref: ReferenceLocatorPipeline
    traits: tuple[Trait, ...] | MISSING = MISSING


class CollectionNode(BaseModel):
    type: Literal["collection"] = "collection"
    id: Id
    name: Name | MISSING = MISSING
    nodes: tuple[CollectionNode | CollectionNodeReference | LeafNodeReference, ...]
    traits: tuple[Trait, ...] | MISSING = MISSING


class CollectionNodeReference(BaseModel):
    type: Literal["collection"] = "collection"
    id: Id
    name: Name | MISSING = MISSING
    ref: ReferenceLocatorPipeline
    traits: tuple[Trait, ...] | MISSING = MISSING


class CustomLeafNode(BaseModel):
    type: Type
    id: Id
    name: Name | MISSING = MISSING
    traits: tuple[Trait, ...] | MISSING = MISSING


class CustomLeafNodeReference(BaseModel):
    type: Type
    id: Id
    name: Name | MISSING = MISSING
    ref: ReferenceLocatorPipeline
    traits: tuple[Trait, ...] | MISSING = MISSING


class SceneTrait(BaseModel):
    type: Literal["scene"] = "scene"
    coordinate_systems: tuple[CoordinateSystem, ...] | MISSING = MISSING
    coordinate_transformations: tuple[CoordinateTransformation, ...]


class CustomTrait(BaseModel):
    type: Type


Trait = Annotated[SceneTrait | CustomTrait, OpenTypeUnion()]

LeafNodeReference = Annotated[
    MultiscaleNodeReference | CustomLeafNodeReference, OpenTypeUnion()
]
Node = Annotated[MultiscaleNode | CollectionNode | CustomLeafNode, OpenTypeUnion()]
NodeReference = Annotated[
    MultiscaleNodeReference | CollectionNodeReference | CustomLeafNodeReference,
    OpenTypeUnion(),
]

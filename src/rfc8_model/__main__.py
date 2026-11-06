from uuid import uuid7

from rfc8_model.aux import StandaloneJson, ZarrJson
from rfc8_model.models import (
    CollectionNode,
    MultiscaleNode,
    MultiscaleNodeItem,
    MultiscaleNodeReference,
    ScaleDownsamplingCoordinateTransformation,
    ZarrPath,
)

multiscale_file = ZarrJson.with_ome(
    MultiscaleNode(
        coordinate_systems=(),
        arrays=(
            MultiscaleNodeArray(
                downsamplingTransformations=(
                    ScaleDownsamplingCoordinateTransformation(
                        scale=(1.0, 1.0, 1.0, 1.0)
                    ),
                )
            ),
            MultiscaleNodeArray(
                downsamplingTransformations=(
                    ScaleDownsamplingCoordinateTransformation(
                        scale=(1.0, 2.0, 2.0, 2.0)
                    ),
                )
            ),
        ),
    )
)


collection_file = StandaloneJson.with_ome(
    CollectionNode(
        id=str(uuid7()),
        nodes=(
            MultiscaleNodeReference(
                id=str(uuid7()),
                path=ZarrPath(format="relative", href=multiscale_file.path),
            ),
        ),
    )
)

print(repr(multiscale_file))
print(repr(collection_file))

from uuid import uuid7

from .aux import StandaloneJson, ZarrJson
from .models import *

multiscale_file = ZarrJson.with_ome(
    MultiscaleNode(
        coordinate_systems=(),
        nodes=(
            MultiscaleNodeItem(
                downsamplingTransformations=(
                    ScaleDownsamplingCoordinateTransformation(
                        scale=(1.0, 1.0, 1.0, 1.0)
                    ),
                )
            ),
            MultiscaleNodeItem(
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
                path=Path(type="zarr", format="relative", href=multiscale_file.path),
            ),
        ),
    )
)

print(repr(multiscale_file))
print(repr(collection_file))

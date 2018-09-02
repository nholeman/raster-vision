import rastervision as rv
from rastervision.task.object_detection_config import ObjectDetectionConfigBuilder
from rastervision.task.chip_classification_config import ChipClassificationConfigBuilder
from rastervision.backend.tf_object_detection_config import TFObjectDetectionConfigBuilder
from rastervision.data.raster_transformer.channel_transformer_config \
    import ChannelTransformerConfigBuilder
from rastervision.data.raster_transformer.stats_transformer_config \
    import StatsTransformerConfigBuilder
from rastervision.protos.task_pb2 import TaskConfig

class RegistryError(Exception):
    pass

class Registry:
    """Singleton that holds instances of Raster Vision types,
       to be referenced by configuration code by key.
    """

    def __init__(self):
        self._internal_config_builders =  {
            # Tasks
            (rv.TASK, rv.OBJECT_DETECTION): ObjectDetectionConfigBuilder,
            (rv.TASK, rv.CHIP_CLASSIFICATION): ChipClassificationConfigBuilder,

            # Backends
            (rv.BACKEND, rv.TF_OBJECT_DETECTION): TFObjectDetectionConfigBuilder,

            # Raster Transformers
            (rv.RASTER_TRANSFORMER, rv.STATS_TRANSFORMER): StatsTransformerConfigBuilder,

            # Raster Sources
            (rv.RASTER_SOURCE, rv.GEOTIFF_SOURCE): rv.data.GeoTiffSourceConfigBuilder,
            (rv.RASTER_SOURCE, rv.IMAGE_SOURCE): rv.data.ImageSourceConfigBuilder
        }

    def get_config_builder(self, group, key):
        internal_builder = self._internal_config_builders.get((group, key))
        if internal_builder:
            return internal_builder
        else:
            # TODO: Search plugins
            pass

        raise RegistryError("Unknown type {} for {} ".format(key, group))

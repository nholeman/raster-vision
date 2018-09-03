from copy import deepcopy

import rastervision as rv
from rastervision.data.raster_source.label_store_config \
    import (LabelStoreConfig, LabelStoreConfigBuilder)
from rastervision.task.util import (construct_classes, classes_to_class_items)
from rastervision.protos.raster_source2_pb2 import LabelStoreConfig as LabelStoreConfigMsg


class ObjectDetectionGeoJSONStoreConfig(LabelStoreConfig):
    def __init__(self, uri, class_map):
        super().__init__(source_type=rv.OBJECT_DETECTION_GEOJSON)
        self.uri = uri

    def to_proto(self):
        msg = super().to_proto()
        opts = LabelStoreConfigMsg.ObjectDetectionGeoJSONFile(self.uri)
        msg.object_detection_geojson_source = opts
        return msg

    def create_source(self, task_config, crs_transformer, tmp_dir):
        return ObjectDetectionGeoJSONStore(self.uri, crs_transformer, task_config.class_map)

class ObjectDetectionGeoJSONStoreConfigBuilder(RasterStoreConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "uri": prev.uri }

        super().__init__(ObjectDetectionGeoJSONStoreConfig, config)

    def from_proto(self, msg):
        b = ObjectDetectionGeoJSONStoreConfigBuilder()

        return b \
            .with_uri(msg.object_detection_geojson_source.uri)

    def with_uri(self, uri):
        b = deepcopy(self)
        b.config['uri'] = uri
        return b

from copy import deepcopy

import rastervision as rv
from rastervision.data.label_source import (LabelSourceConfig,
                                            LabelSourceConfigBuilder,
                                            ObjectDetectionGeoJSONSource)
from rastervision.protos.label_source_pb2 import LabelSourceConfig as LabelSourceConfigMsg


class ObjectDetectionGeoJSONSourceConfig(LabelSourceConfig):
    def __init__(self, uri):
        super().__init__(source_type=rv.OBJECT_DETECTION_GEOJSON)
        self.uri = uri

    def to_proto(self):
        msg = super().to_proto()
        opts = LabelSourceConfigMsg.ObjectDetectionGeoJSONSource(uri=self.uri)
        msg.object_detection_geojson_source.CopyFrom(opts)
        return msg

    def create_source(self, task_config, crs_transformer, tmp_dir):
        return ObjectDetectionGeoJSONSource(self.uri, crs_transformer, task_config.class_map)

    def preprocess_command(self, command_type, experiment_config, context=[]):
        io_def = rv.core.CommandIODefinition()
        io_def.add_input(self.uri)

        return (self, io_def)


class ObjectDetectionGeoJSONSourceConfigBuilder(LabelSourceConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "uri": prev.uri }

        super().__init__(ObjectDetectionGeoJSONSourceConfig, config)

    def from_proto(self, msg):
        b = ObjectDetectionGeoJSONSourceConfigBuilder()

        return b \
            .with_uri(msg.object_detection_geojson_source.uri)

    def with_uri(self, uri):
        b = deepcopy(self)
        b.config['uri'] = uri
        return b

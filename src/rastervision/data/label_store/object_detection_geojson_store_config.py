from copy import deepcopy

import rastervision as rv
from rastervision.data.raster_source.label_store_config \
    import (LabelStoreConfig, LabelStoreConfigBuilder)
from rastervision.task.util import (construct_classes, classes_to_class_items)
from rastervision.protos.raster_source2_pb2 import LabelStoreConfig as LabelStoreConfigMsg


class ObjectDetectionGeoJSONStoreConfig(LabelStoreConfig):
    def __init__(self, uri):
        super().__init__(source_type=rv.OBJECT_DETECTION_GEOJSON)
        self.uri = uri

    def to_proto(self):
        msg = super().to_proto()
        opts = LabelStoreConfigMsg.ObjectDetectionGeoJSONFile(self.uri)
        msg.object_detection_geojson_source = opts
        return msg

    def create_source(self, task_config, crs_transformer, tmp_dir):
        return ObjectDetectionGeoJSONStore(self.uri, crs_transformer, task_config.class_map)

    def preprocess_command(self, command_type, experiment_config, context=[]):
        conf = self
        io_def = rv.core.CommandIODefinition()

        if command_type == rv.PREDICT:
            if not self.uri:
                # Construct the  URI for this prediction store,
                # using the scene ID.
                root = experiment_config.predict_uri
                uri = None
                for c in context:
                    if isinstance(c, rv.SceneConfig):
                        uri = os.path.join(root, "{}.json".format(c.scene_id))
                if uri:
                    conf = conf.builder() \
                               .with_uri(uri) \
                               .builder()
                    io_def.add_output(uri)
                else:
                    raise rv.ConfigError("ObjectDetectionGeoJSONStoreConfig has no "
                                         "URI set, and is not associated with a SceneConfig.")

            io_def.add_output(conf.uri)

        if command_type == rv.EVAL:
            if self.uri:
                io_def.add_input(self.uri)
            else:
                msg = "No URI set for ObjectDetectionGeoJSONStoreConfig"
                io_def.add_missing(msg)

        return (conf, io_def)


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

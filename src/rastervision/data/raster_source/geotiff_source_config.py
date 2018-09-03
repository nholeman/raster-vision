from copy import deepcopy

import rastervision as rv
from rastervision.data.raster_source.geotiff_source import GeoTiffSource
from rastervision.data.raster_source.raster_source_config \
    import (RasterSourceConfig, RasterSourceConfigBuilder)
from rastervision.protos.raster_source2_pb2 import RasterSourceConfig as RasterSourceConfigMsg
from rastervision.utils.files import file_exists


class GeoTiffSourceConfig(RasterSourceConfig):
    def __init__(self,
                 uris,
                 transformers=[],
                 channel_order=None):
        super().__init__(source_type=rv.GEOTIFF_SOURCE,
                         transformers=transformers,
                         channel_order=channel_order)
        self.uris = uris

    def to_proto(self):
        msg = super().to_proto()
        msg.geotiff_files.CopyFrom(RasterSourceConfigMsg.GeoTiffFiles(uris=self.uris))
        return msg

    def create_source(self, tmp_dir):
        transformers = self.create_transformers()
        return GeoTiffSource(self.uris, transformers, tmp_dir, self.channel_order)

    # TODO
    def traverse(self, command, experiment_config):
        dependencies = rv.core.CommandIODefinition()
        dependencies.add_input(command, self.uris)
        transformers = []
        for t in self.transformers:
            d, new_t = t.traverse(command, experiment_config)
            dependencies = dependencies + d
            transformers.append(new_t)
        return dependencies, self.builder() \
                                 .with_transformers(transformers) \
                                 .build()


class GeoTiffSourceConfigBuilder(RasterSourceConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "uris": prev.uris,
                       "transformers": prev.transformers,
                       "channel_order": prev.channel_order }

        super().__init__(GeoTiffSourceConfig, config)

    def from_proto(self, msg):
        b = super().from_proto(msg)

        return b \
            .with_uris(msg.geotiff_files.uris)

    def with_uris(self, uris):
        b = deepcopy(self)
        b.config['uris'] = uris
        return b

    def with_uri(self, uri):
        b = deepcopy(self)
        b.config['uris'] = [uri]
        return b

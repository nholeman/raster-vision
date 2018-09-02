from copy import deepcopy

import rastervision as rv
from rastervision.core.raster_stats import RasterStats
from rastervision.data.raster_transformer.stats_transformer import StatsTransformer
from rastervision.data.raster_transformer.raster_transformer_config \
    import (RasterTransformerConfig, RasterTransformerConfigBuilder)
from rastervision.protos.raster_transformer2_pb2 import RasterTransformerConfig as RasterTransformerConfigMsg

class StatsTransformerConfig(RasterTransformerConfig):
    def __init__(self, stats_uri=None):
        super().__init__(rv.STATS_TRANSFORMER)
        self.stats_uri = stats_uri

    def to_proto(self):
        conf = RasterTransformerConfig(transformer_type=self.transformer_type,
                                       stats_uri=self.stats_uri)
        return conf

    def builder(self):
        return StatsTransformerConfigBuilder(self)

    def create_transformer(self):
        return StatsTransformer(RasterStats.load(self.stats_uri))

class StatsTransformerConfigBuilder(RasterTransformerConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "stats_uri": prev.stats_uri }
        super().__init__(StatsTransformerConfig, config)

    @staticmethod
    def from_proto(self, msg):
        conf = msg.stats_uri
        b = StatsTransformerConfigBuilder()
        return b.with_stats_uri(conf.stats_uri)

    def with_stats_uri(self, stats_uri):
        """Set the stats_uri.

            Args:
                stats_uri: URI to the stats json to use
        """
        b = deepcopy(self)
        b.config['stats_uri'] = stats_uri
        return b

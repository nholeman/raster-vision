from copy import deepcopy

import rastervision as rv
from rastervision.data.raster_transformer.channel_transformer import ChannelTransformer
from rastervision.data.raster_transformer.raster_transformer_config \
    import (RasterTransformerConfig, RasterTransformerConfigBuilder)
from rastervision.protos.raster_transformer2_pb2 import RasterTransformerConfig as RasterTransformerConfigMsg

class ChannelTransformerConfig(RasterTransformerConfig):
    def __init__(self):
        super().__init__(rv.CHANNEL_TRANSFORMER)
        self.channel_order = None

    def to_proto(self):
        channel_transformer_config = RasterTransformerConfig \
                                     .ChannelTransformerConfig(
                                         channel_order=self.channel_order)

        conf = RasterTransformerConfig(transformer_type=self.transformer_type,
                                       channel_transformer_config=channel_transformer_config)
        return conf

    def builder(self):
        return ChannelTransformerConfigBuilder(self)

    def create_transformer(self):
        return ChannelTransformer(self.channel_order)

class ChannelTransformerConfigBuilder(RasterTransformerConfigBuilder):
    def __init__(self, config=None):
        super().__init__(config or ChannelTransformerConfig())
        self.channel_order = None

    def from_proto(self, msg):
        conf = msg.channel_transformer_config
        b = ChannelTransformerConfigBuilder()
        return b.with_channel_order(conf.channel_order)

    # TODO: better validation logic - how do we pass errors up and concatenate?
    def validate(self, validate_uris=True):
        if not self.config.channel_order:
            raise rv.ConfigError("ChannelTransformer requires channel order, use with_channel_order")
        return True

    def with_channel_order(self, channel_order):
        """Set the channel order for this transformer.
        """
        c = deepcopy(self.config)
        c.channel_order = channel_order
        return ChannelTransformerConfigBuilder(c)

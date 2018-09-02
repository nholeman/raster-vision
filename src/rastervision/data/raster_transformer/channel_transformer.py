from .raster_transformer import RasterTransformer

class ChannelTransformer(RasterTransformer):
    """Transform raster data by subsetting or reordering channels.
    """
    def __init__(self, channel_order=None):
        """Construct a new ChannelTransformer.

        Args:
            channel_order: numpy array of length n where n is the number of
                channels to use and the values are channel indices
        """
        self.channel_order = channel_order

    def transform(self, chip):
        """Transform a chip.

        Reorder and selects a subset of the channels.

        Args:
            chip: [height, width, channels] numpy array

        Returns:
            [height, width, channels] numpy array where channels is equal
                to len(channel_order)
        """
        if self.channel_order is None:
            channel_order = np.arange(chip.shape[2])
        else:
            channel_order = self.channel_order

        return chip[:, :, channel_order]

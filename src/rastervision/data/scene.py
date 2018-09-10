class Scene():
    """The raster data and labels associated with an area of interest."""

    # TODO: Make id vs scene_id consistent across library
    def __init__(self,
                 scene_id,
                 raster_source,
                 ground_truth_label_source=None,
                 prediction_label_store=None):
        """Construct a new Scene.

        Args:
            scene_id: ID for this scene
            raster_source: RasterSource for this scene
            ground_truth_label_store: optional LabelSource
            prediction_label_store: optional LabelStore
        """
        self.scene_id = scene_id
        self.raster_source = raster_source
        self.ground_truth_label_store = ground_truth_label_store
        self.prediction_label_store = prediction_label_store
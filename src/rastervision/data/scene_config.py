from copy import deepcopy
from typing import Union

import rastervision as rv
from rastervision.core import (Config, ConfigBuilder)
from rastervision.task import TaskConfig
from rastervision.data import (Scene,
                               RasterSourceConfig,
                               LabelSourceConfig,
                               LabelStoreConfig)
from rastervision.protos.scene2_pb2 import SceneConfig as SceneConfigMsg

class SceneConfig(Config):
    def __init__(self,
                 scene_id,
                 raster_source,
                 label_source=None,
                 label_store=None):
        self.scene_id = scene_id
        self.raster_source = raster_source
        self.label_source = label_source
        self.label_store = label_store

    def create_scene(self, task_config: TaskConfig, tmp_dir: str) -> Scene:
        """Create this scene.

           Args:
              task - TaskConfig
              tmp_dir - Temporary directory to use
        """
        raster_source = self.raster_source.create_source(tmp_dir)
        label_source = None
        if self.label_source:
            label_source = self.label_source.create_source(task_config,
                                                           raster_source.get_crs_transformer(),
                                                           tmp_dir)
        label_store = None
        if self.label_store:
            label_store = self.label_source.create_store(task_config,
                                                         raster_source.get_crs_transformer(),
                                                         tmp_dir)
        return Scene(self.scene_id,
                     raster_source,
                     label_source,
                     label_store)

    def to_proto(self):
        msg = SceneConfigMsg( raster_source = self.raster_source.to_proto())

        if self.label_source:
            msg.ground_truth_label_source.CopyFrom(self.label_source.to_proto())
        if self.label_store:
            msg.prediction_label_store.CopyFrom(self.label_store.to_proto())
        return msg

    def builder(self):
        return SceneConfigBuilder(self)

    @staticmethod
    def builder():
        return SceneConfigBuilder()

    @staticmethod
    def from_proto(msg):
        """Creates a SceneConfig from the specificed protobuf message
        """
        return SceneConfigBuilder().from_proto(msg).build()

class SceneConfigBuilder(ConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "scene_id": prev.scene_id,
                       "raster_source": prev.raster_source,
                       "label_source": prev.label_source,
                       "label_store": prev.label_store }
        super().__init__(SceneConfig, config)
        self.task = None

    def from_proto(self, msg):
        b = self.with_id(msg.id) \
                .with_raster_source(RasterSourceConfig.from_proto(msg.raster_source))
        if msg.HasField('ground_truth_label_source'):
            b = b.with_label_source(
                LabelSourceConfig.from_proto(msg.ground_truth_label_source))
        if msg.HasField('prediction_label_store'):
            b = b.with_label_store(
                LabelStoreConfig.from_proto(msg.prediction_label_store)  )

        return b

    def with_task(self, task):
        b = deepcopy(self)
        b.task = task
        return b

    def with_id(self, scene_id):
        b = deepcopy(self)
        b.config['scene_id'] = scene_id
        return b

    def with_raster_source(self,
                           raster_source: Union[str, RasterSourceConfig],
                           channel_order=None):
        """
        Sets the raster source for this scene.

        Args:
           raster_source: Can either be a raster source configuration, or
                          a string. If a string, the registry will be queried
                          to grab the default RasterSourceConfig for the string.
           channel_order: Optional channel order for this raster source.
        """
        b = deepcopy(self)
        if isinstance(raster_source, RasterSourceConfig):
            if channel_order is not None:
                b.config['raster_source'] = raster_source.builder() \
                                                         .with_channel_order(channel_order) \
                                                         .build()
            else:
                b.config['raster_source'] = raster_source
        else:
            provider = rv._registry.get_default_raster_source_provider(raster_source)
            b.config['raster_source'] = provider.construct(raster_source, channel_order)


        return b

    def with_label_source(self, label_source: Union[str, LabelSourceConfig]):
        """
        Sets the raster source for this scene.

        Args:
           label_source: Can either be a label source configuration, or
                         a string. If a string, the registry will be queried
                         to grab the default LabelSourceConfig for the string.

        Note:
           A task must be set with `with_task` before calling this, if calling
           with a string.
        """
        b = deepcopy(self)
        if isinstance(label_source, LabelSourceConfig):
            b.config['label_source'] = label_source
        else:
            if not self.task:
                raise rv.ConfigError("You must set a task with '.with_task' before "
                                     "creating a default label store for {}".format(label_source))
            provider = rv._registry.get_default_label_source_provider(self.task.task_type,
                                                                      label_source)
            b.config['label_source'] = provider.construct(label_source)


        return b

    def with_label_store(self, label_store: Union[str, LabelStoreConfig]):
        """
        Sets the raster store for this scene.

        Args:
           label_store: Can either be a label store configuration, or
                        a string. If a string, the registry will be queried
                        to grab the default LabelStoreConfig for the string.

        Note:
           A task must be set with `with_task` before calling this, if calling
           with a string.
        """
        # TODO
        b = deepcopy(self)
        if isinstance(label_source, LabelSourceConfig):
            b.config['label_source'] = label_source
        else:
            if not self.task:
                raise rv.ConfigError("You must set a task with '.with_task' before "
                                     "creating a default label store for {}".format(label_source))
            provider = rv._registry.get_default_label_source_provider(self.task.task_type,
                                                                      label_source)
            b.config['label_source'] = provider.construct(label_source)


        return b

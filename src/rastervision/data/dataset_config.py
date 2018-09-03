from copy import deepcopy

from rastervision.data import SceneConfig
from rastervision.core.config  import (Config, ConfigBuilder)
from rastervision.protos.dataset_pb2 import DatasetConfig as DatasetConfigMsg

class DatasetConfig(Config):
    def __init__(self,
                 train_scenes=[],
                 validation_scenes=[],
                 test_scenes=[]):
        self.train_scenes = train_scenes
        self.validation_scenes = validation_scenes
        self.test_scenes = test_scenes

    def builder(self):
        return DatasetConfigBuilder(self)

    def create_dataset(self,
                       task_config,
                       tmp_dir,
                       include_train=True,
                       include_val=True,
                       include_test=True):
        train_scenes = []
        if include_train:
            train_scenes = list(map(lambda x: x.create_scene(task_config, tmp_dir),
                                    self.train_scenes))

        val_scenes = []
        if include_val:
            val_scenes = list(map(lambda x: x.create_scene(task_config, tmp_dir),
                                  self.validaiton_scenes))

        test_sceness = []
        if include_test:
            test_scenes = list(map(lambda x: x.create_scene(task_config, tmp_dir),
                                   self.test_scenes))
        return DataSet(train_scenes=train_scenes,
                       validation_scenes=val_scenes,
                       test_scenes=test_scenes)

    def to_proto(self):
        """Returns the protobuf configuration for this config.
        """
        train_scenes = list(map(lambda x: x.to_proto(),
                                   self.train_scenes))
        val_scenes = list(map(lambda x: x.to_proto(),
                                   self.validation_scenes))
        test_scenes = list(map(lambda x: x.to_proto(),
                                   self.test_scenes))

        return DatasetConfigMsg(train_scenes=train_scenes,
                                validation_scenes=val_scenes,
                                test_scenes=test_scenes)

    @staticmethod
    def from_proto(msg):
        """Creates a TaskConfig from the specificed protobuf message
        """
        return DatasetConfigBuilder().from_proto(msg).build()

    @staticmethod
    def builder():
        return DatasetConfigBuilder()

class DatasetConfigBuilder(ConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config['train_scenes'] = prev.train_scenes
            config['validation_scenes'] = prev.validation_scenes
            config['test_scenes'] = prev.test_scenes
        super().__init__(DatasetConfig, config)

    def from_proto(self, msg):
        train_scenes = list(map(lambda x: SceneConfig.from_proto(x),
                                   msg.train_scenes))
        val_scenes = list(map(lambda x: SceneConfig.from_proto(x),
                                   msg.validation_scenes))
        test_scenes = list(map(lambda x: SceneConfig.from_proto(x),
                                   msg.test_scenes))
        return DatasetConfigBuilder() \
            .with_train_scenes(train_scenes) \
            .with_validation_scenes(val_scenes) \
            .with_test_scenes(test_scenes)

    def with_train_scenes(self, scenes):
        b = deepcopy(self)
        b.config['train_scenes'] = scenes
        return b

    def with_train_scene(self, scene):
        return self.with_train_scenes([scene])

    def with_validation_scenes(self, scenes):
        b = deepcopy(self)
        b.config['validation_scenes'] = scenes
        return b

    def with_validation_scene(self, scene):
        return self.with_validation_scenes([scene])

    def with_test_scenes(self, scenes):
        b = deepcopy(self)
        b.config['test_scenes'] = scenes
        return b

    def with_test_scene(self, scene):
        return self.with_test_scene([scene])

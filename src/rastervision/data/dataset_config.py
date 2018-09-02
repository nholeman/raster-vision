from copy import deepcopy

from rastervision.core.config  import (Config, ConfigBuilder)

class DatasetConfig(Config):
    def __init__(self,
                 train_scenes=[],
                 validation_scenes=[],
                 test_scenes=[]):
        self.train_scenes = training_scenes
        self.validation_scenes = validation_scenes
        self.test_scenes = test_scenes

    def builder(self):
        return DatasetConfigBuilder(self)

    def create_dataset(self):
        DataSet(
            train_scenes=list(map(lambda x: x.create_scene(),
                                  self.train_scenes)),
            validation_scenes=list(map(lambda x: x.create_scene(),
                                       self.validaiton_scenes)),
            test_scenes=list(map(lambda x: x.create_scene(),
                                 self.validation_scenes)))

    def to_proto(self):
        """Returns the protobuf configuration for this config.
        """
        pass

    @staticmethod
    def from_proto(msg):
        """Creates a TaskConfig from the specificed protobuf message
        """
        pass

    @staticmethod
    def builder():
        return DatasetConfigBuilder()

class DatasetConfigBuilder(ConfiBuilder):
    def __init__(self, config=None):
        super().__init__(config or DatasetConfig())

    def validate(self):
        # All values default
        return True

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
        d = deepcopy(self.config)
        d.train_scenes = scenes
        return DatasetConfigBuilder(d)

    def with_validation_scenes(self, scenes):
        d = deepcopy(self.config)
        d.validation_scenes = scenes
        return DatasetConfigBuilder(d)

    def with_test_scenes(self, scenes):
        d = deepcopy(self.config)
        d.test_scenes = scenes
        return DatasetConfigBuilder(d)

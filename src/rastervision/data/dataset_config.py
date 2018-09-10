from copy import deepcopy

from rastervision.augmentor import AugmentorConfig
from rastervision.data import SceneConfig
from rastervision.core.config  import (Config, ConfigBuilder)
from rastervision.protos.dataset_pb2 import DatasetConfig as DatasetConfigMsg

class DatasetConfig(Config):
    def __init__(self,
                 train_scenes=[],
                 validation_scenes=[],
                 test_scenes=[],
                 augmentors=[]):
        self.train_scenes = train_scenes
        self.validation_scenes = validation_scenes
        self.test_scenes = test_scenes
        self.augmentors = augmentors

    def all_scenes(self):
        return self.train_scenes + \
            self.validation_sceness + \
            self.test_scenes

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

        augmentors = list(map(lambda x: x.create_augmentor(),
                              self.augmentors))

        return DataSet(train_scenes=train_scenes,
                       validation_scenes=val_scenes,
                       test_scenes=test_scenes,
                       augmentors=augmentors)

    def to_proto(self):
        """Returns the protobuf configuration for this config.
        """
        train_scenes = list(map(lambda x: x.to_proto(),
                                self.train_scenes))
        val_scenes = list(map(lambda x: x.to_proto(),
                              self.validation_scenes))
        test_scenes = list(map(lambda x: x.to_proto(),
                               self.test_scenes))

        augmentors = list(map(lambda x: x.to_proto(),
                              self.augmentors))

        return DatasetConfigMsg(train_scenes=train_scenes,
                                validation_scenes=val_scenes,
                                test_scenes=test_scenes,
                                augmentors = augmentors)

    def preprocess_command(self, command_type, experiment_config, context=[]):
        io_def = CommandIODefinition()
        train_scenes = []
        for scene in self.train_scenes:
            (scene_io_def, new_config) = scene.process_experiment_for_command(command_type,
                                                                              experiment_config,
                                                                              context)
            io_def.merge(scene_io_def)
            train_scenes.append(new_config)

        val_scenes = []
        for scene in self.validation_scenes:
            if command_type == rv.PREDICT:
                # Ensure there is a label store associated with predict and validation scenes.
                if not scene.label_store:
                    scene = scene.builder() \
                                 .with_task(experiment_config.task) \
                                 .with_label_store() \
                                 .build()
            (scene_io_def, new_config) = scene.preprocess_command(command_type,
                                                                  experiment_config,
                                                                  context)
            io_def.merge(scene_io_def)
            val_scenes.append(new_config)

        predict_scenes = []
        for scene in self.predict_scenes:
            if command_type == rv.PREDICT:
                # Ensure there is a label store associated with predict and validation scenes.
                if not scene.label_store:
                    scene = scene.builder() \
                                 .with_task(experiment_config.task) \
                                 .with_label_store() \
                                 .build()
            (scene_io_def, new_config) = scene.preprocess_command(command_type,
                                                                  experiment_config,
                                                                  context)
            io_def.merge(scene_io_def)
            predict_scenes.append(new_config)

        augmentors = []
        for augmentor in self.augmentors:
            (aug_io_def, new_config) = augmentor.preprocess_command(command_type,
                                                                    experiment_config,
                                                                    context)
            io_def.merge(aug_io_def)
            augmentors.append(new_config)

        conf = self.builder().with_train_scenes(train_scenes) \
                             .with_val_scenes(val_scenes) \
                             .with_predict_scenes(predict_scenes) \
                             .with_augmentors(augmentors) \
                             .build()

        return (conf, io_def)

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
        config = {
            'train_scenes': [],
            'validation_scenes': [],
            'test_scenes': [],
            'augmentors': []
        }
        if prev:
            config['train_scenes'] = prev.train_scenes
            config['validation_scenes'] = prev.validation_scenes
            config['test_scenes'] = prev.test_scenes
            config['augmentors'] = prev.augmentors
        super().__init__(DatasetConfig, config)

    def from_proto(self, msg):
        train_scenes = list(map(lambda x: SceneConfig.from_proto(x),
                                   msg.train_scenes))
        val_scenes = list(map(lambda x: SceneConfig.from_proto(x),
                                   msg.validation_scenes))
        test_scenes = list(map(lambda x: SceneConfig.from_proto(x),
                                   msg.test_scenes))
        augmentors = list(map(lambda x: AugmentorConfig.from_proto(x),
                              msg.augmentors))
        return DatasetConfigBuilder() \
            .with_train_scenes(train_scenes) \
            .with_validation_scenes(val_scenes) \
            .with_test_scenes(test_scenes) \
            .with_augmentors(augmentors)

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
        return self.with_test_scenes([scene])

    def with_augmentors(self, augmentors):
        b = deepcopy(self)
        b.config['augmentors'] = augmentors
        return b

    def with_augmentor(self, augmentor):
        return with_augmentors([augmentor])

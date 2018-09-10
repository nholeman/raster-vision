from copy import deepcopy

import rastervision as rv
from rastervision.command import (ChipCommand,
                                  CommandConfig,
                                  CommandConfigBuilder,
                                  NoOpCommand)
from rastervision.protos.chip_command_pb2 \
    import ChipCommandConfig as ChipCommandConfigMsg

class ChipCommandConfig(CommandConfig):
    def __init__(self,
                 task,
                 backend,
                 train_scenes,
                 val_scenes):
        super.__init__(rv.CHIP)
        self.task = task
        self.backend = backend
        self.train_scenes = train_scenes
        self.val_scenes = val_scenes

    def create_command(self, tmp_dir):
        if len(self.train_scenes) == 0 and len(self.val_scenes) == 0:
            return NoOpCommand()

        backend = self.backend.create_backend(self.task)
        task = self.task.create_tasks(backend)

        train_scenes = list(map(lambda s: s.create_scene(self.task, tmp_dir),
                                self.train_scenes))
        val_scenes = list(map(lambda s: s.create_scene(self.task, tmp_dir),
                              self.val_scenes))

        return ChipCommand(task, train_scenes, val_scenes)

    def to_proto(self):
        msg = super().to_proto()

        task = self.task.to_proto()
        backend = self.backend.to_proto()
        train_scenes = list(map(lambda s: s.to_proto(), self.train_scenes))
        val_scenes = list(map(lambda s: s.to_proto(), self.val_scenes))

        msg.SetField("chip_config",
                     CommandConfigMsg.ChipConfig(task=task,
                                                 backend=backend,
                                                 train_scenes=train_scenes,
                                                 val_scenes=val_scenes))

        return msg

    @staticmethod
    def builder():
        return ChipCommandConfigBuilder()

class ChipCommandConfigBuilder(CommandConfigBuilder):
    def __init__(self):
        self.task = None
        self.backend = None
        self.train_scenes = []
        self.val_scenes = []

    def build(self):
        if self.task is None:
            raise rv.ConfigError("Task not set. Use with_task or with_experiment")

        if self.backend is None:
            raise rv.ConfigError("Backend not set. Use with_backend or with_experiment")

        return ChipCommandConfig(self.train_scenes,
                                 self.val_scenes,
                                 self.task)


    def from_proto(self, msg):
        msg = msg.chip_config

        task = rv.TaskConfig.from_proto(msg.task)
        backend = rv.BackendConfig.from_proto(msg.backend)
        train_scenes = list(map(rv.SceneConfig.from_proto,
                                msg.train_scenes))
        val_scenes = list(map(rv.SceneConfig.from_proto,
                                msg.train_scenes))

        b = self.with_task(task)
        b = b.with_backend(backend)
        b = b.with_train_scenes(train_scenes)
        b = b.with_val_sceness(val_scenes)

        return b

    def with_experiment(self, experiment_config):
        b = self.with_task(experiment_config.task)
        b = b.with_train_scenes(experiment_config.dataset.train_scenes)
        b = b.with_val_scenes(experiment_config.dataset.val_scenes)
        return  b

    def with_task(self, task):
        b = deepcopy(b)
        b.task = task
        return b

    def with_backend(self, backend):
        b = deepcopy(b)
        b.backend = backend
        return b


    def with_train_scenes(self, scenes):
        b = deepcopy(b)
        b.train_scenes = scenes
        return b

    def with_val_scenes(self, scenes):
        b = deepcopy(b)
        b.val_scenes = scenes
        return b

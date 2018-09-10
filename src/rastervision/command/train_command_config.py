from copy import deepcopy

import rastervision as rv
from rastervision.command import (TrainCommand,
                                  CommandConfig,
                                  CommandConfigBuilder,
                                  NoOpCommand)
from rastervision.protos.train_command_pb2 \
    import TrainCommandConfig as TrainCommandConfigMsg

class TrainCommandConfig(CommandConfig):
    def __init__(self,
                 task,
                 backend):
        self.task = task
        self.backend = backend

    def create_command(self, tmp_dir):
        backend = self.backend.create_backend(self.task)
        task = self.task.create_tasks(backend)

        return TrainCommand(task)

    def to_proto(self):
        msg = super().to_proto()

        task = self.task.to_proto()
        backend = self.backend.to_proto()

        msg.SetField("train_config",
                     CommandConfigMsg.TrainConfig(task=task,
                                                  train_scenes=train_scenes,
                                                  val_scenes=val_scenes))

        return msg

    @staticmethod
    def builder():
        return TrainCommandConfigBuilder()

class TrainCommandConfigBuilder(CommandConfigBuilder):
    def __init__(self):
        self.train_scenes = []
        self.val_scenes = []
        self.task = None

    def build(self):
        if self.task is None:
            raise rv.ConfigError("task not set. Use with_task or with_experiment")

        return TrainCommandConfig(self.train_scenes,
                                 self.val_scenes,
                                 self.task)


    def from_proto(self, msg):
        task = rv.TaskConfig.from_proto(msg.task)
        train_scenes = list(map(rv.SceneConfig.from_proto,
                                msg.train_scenes))
        val_scenes = list(map(rv.SceneConfig.from_proto,
                                msg.train_scenes))

        b = self.with_task(task)
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
        b.task_config = task
        return b

    def with_train_scenes(self, scenes):
        b = deepcopy(b)
        b.train_scenes = scenes
        return b

    def with_val_scenes(self, scenes):
        b = deepcopy(b)
        b.val_scenes = scenes
        return b

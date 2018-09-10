from copy import deepcopy

import rastervision as rv
from rastervision.command import (AnalyzeCommand,
                                  CommandConfig,
                                  CommandConfigBuilder,
                                  NoOpCommand)
from rastervision.protos.command_pb2 \
    import CommandConfig as CommandConfigMsg

class AnalyzeCommandConfig(CommandConfig):
    def __init__(self,
                 task,
                 scenes,
                 analyzers):
        super().__init__(self, rv.ANALYZE)
        self.task_config = task
        self.scenes = scenes
        self.analyzers = analyzers

    def create_command(self, tmp_dir):
        if len(self.scenes) == 0 or len(self.analyzers) == 0:
            return NoOpCommand()

        scenes = list(map(lambda s: s.create_scene(self.task, tmp_dir),
                          self.scenes))
        analyzers = list(map(lambda a: a.create_analyzer(),
                             self.analyzers))
        return AnalyzeCommand(scenes, analyzers)

    def to_proto(self):
        msg = super().to_proto()
        task = self.task.to_proto()
        scenes = list(map(lambda s: s.to_proto(), self.scenes))
        analyzers = list(map(lambda a: a.to_proto(), self.analyzers))

        msg.SetField("analyze_config",
                     CommandConfig.AnalyzeConfig(task=task,
                                                 scenes=scenes,
                                                 analyzers=analyzers))

        return msg

    @staticmethod
    def builder():
        return AnalyzeCommandConfigBuilder()

class AnalyzeCommandConfigBuilder(CommandConfigBuilder):
    def __init__(self):
        self.task_config = None
        self.scene_configs = None
        self.analyzer_configs = None

    def build(self):
        if self.task_config is None:
            raise rv.ConfigError("task not set. Use with_task or with_experiment")
        if self.scenes is None:
            raise rv.ConfigError("scenes not set. Use with_scenes or with_experiment")
        if self.analyzers is None:
            raise rv.ConfigError("analyzers not set. Use with_analyzers or with_experiment")
        return AnalyzerCommandConfig(self.task_config,
                                     self.scene_configs,
                                     self.analyzer_configs)


    def from_proto(self, msg):
        msg = msg.analyze_config

        task = rv.TaskConfig.from_proto(msg.task)
        scenes = list(map(rv.SceneConfig.from_proto,
                          msg.scenes))
        analyzers = list(map(rv.AnalyzerConfig.from_proto,
                             msg.analyzers))

        b = self.with_task(task)
        b = b.with_scenes(scenes)
        b = b.with_analyzers(analyzers)

        return b

    def with_experiment(self, experiment_config):
        b = self.with_task(experiment_config.task)
        b = b.with_scenes(experiment_config.dataset.all_scenes())
        b = b.with_analyzers(experiment_config.analyzers)
        return  b

    def with_task(self, task):
        b = deepcopy(b)
        b.task_config = task
        return b

    def with_scenes(self, scenes):
        b = deepcopy(b)
        b.scene_configs = scenes
        return b

    def with_analyzers(self, analyzers):
        b = deepcopy(b)
        b.analyzer_configs = analyzers
        return b

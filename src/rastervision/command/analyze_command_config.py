from copy import deepcopy

from rastervision.command import (AnalyzeCommand,
                                  CommandConfig,
                                  CommandConfigBuilder,
                                  NoOpCommand)

class AnalyzeCommandConfig(CommandConfig):
    def __init__(self,
                 task_config,
                 scene_configs,
                 analyzer_configs):
        self.task_config = task_config
        self.scene_configs = scene_configs
        self.analyzer_configs = analyzer_configs

    def create_command(self, tmp_dir):
        if len(self.scene_configs) == 0 or len(self.analyzer_configs) == 0:
            return NoOpCommand()

        scenes = list(map(lambda s: s.create_scene(self.task_config, tmp_dir),
                          self.scene_configs))
        analyzers = list(map(lambda a: a.create_analyzer(),
                             self.analyzer_configs))
        return AnalyzeCommand(scenes, analyzers)

    def to_proto(self):
        pass

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
        pass

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

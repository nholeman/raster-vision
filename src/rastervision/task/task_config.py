from abc import (ABC, abstractmethod)
from copy import deepcopy

import rastervision as rv
from rastervision.core import (Config, ConfigBuilder)

class TaskConfig(Config):
    def __init__(self, task_type):
        self.task_type = task_type

    @abstractmethod
    def create_task(self, backend):
        """Create the Task that this configuration represents

           Args:
              backend: The backend to be used by the task.
        """
        pass

    @staticmethod
    def builder(task_type):
        return rv._registry.get_config_builder(rv.TASK, task_type)()

    @staticmethod
    def from_proto(msg):
        """Creates a TaskConfig from the specificed protobuf message
        """
        return rv._registry.get_config_builder(rv.TASK, msg.task_type)() \
                           .from_proto(msg) \
                           .build()

    def preprocess_command(self,
                           command_type,
                           experiment_config,
                           context=[]):
        # Generally tasks do now have an affect on the IO.
        return (self, rv.core.CommandIODefinition())

class TaskConfigBuilder(ConfigBuilder):
    """Currently doesn't add anything to ConfigBuilder
    """
    pass

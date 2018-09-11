from abc import (ABC, abstractmethod)
from copy import deepcopy

import rastervision as rv
from rastervision.core import (Config, ConfigBuilder)

class TaskConfig(Config):
    def __init__(self, task_type, predict_batch_size=10):
        self.task_type = task_type
        self.predict_batch_size = predict_batch_size

    @abstractmethod
    def create_task(self, backend):
        """Create the Task that this configuration represents

           Args:
              backend: The backend to be used by the task.
        """
        pass

    def to_builder(self):
        return rv._registry.get_config_builder(rv.TASK,
                                               self.task_type)(self)

    @staticmethod
    def builder(task_type):
        return rv._registry.get_config_builder(rv.TASK,
                                               task_type)()

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
                           context=None):
        # Generally tasks do now have an affect on the IO.
        return (self, rv.core.CommandIODefinition())

class TaskConfigBuilder(ConfigBuilder):
    def with_predict_batch_size(self, predict_batch_size):
        """Sets the batch size to use during prediction."""
        b = deepcopy(self)
        b.config['predict_batch_size'] = predict_batch_size
        return b

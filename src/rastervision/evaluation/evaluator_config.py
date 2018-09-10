from abc import abstractmethod

from rastervision.core import (Config, ConfigBuilder)

class EvaluatorConfig:
    def __init__(self, evaluator_type):
        self.evaluator_type = evaluator_type

    @abstractmethod
    def create_evaluator(self):
        """Create the Evaluator that this configuration represents"""
        pass

    @staticmethod
    def builder(evaluator_type):
        return rv._registry.get_config_builder(rv.EVALUATOR, evaluator_type)()

    @staticmethod
    def from_proto(msg):
        """Creates a EvaluatorConfig from the specificed protobuf message
        """
        return rv._registry.get_config_builder(rv.EVALUATOR, msg.evaluator_type)() \
                           .from_proto(msg) \
                           .build()

    def preprocess_command(self,
                           command_type,
                           experiment_config,
                           context=[]):
        # Generally evaluators do not have an affect on the IO.
        return (self, rv.core.CommandIODefinition())

class EvaluatorConfigBuilder(ConfigBuilder):
    pass

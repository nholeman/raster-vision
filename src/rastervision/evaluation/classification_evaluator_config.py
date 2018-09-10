import os

import rastervision as rv
from rastervision.evaluation import (EvaluatorConfig,
                                     EvaluatorConfigBuilder,
                                     ClassificationEvaluator)
from rastervision.protos.evaluator_pb2 import EvaluatorConfig as EvaluatorConfigMsg

class ClassificationEvaluatorConfig(EvaluatorConfig):
    def  __init__(self, eval_uri=None):
        super().__init__(rv.CLASSIFICATION_EVALUATOR)
        self.eval_uri = eval_uri

    def create_evaluator(self):
        if not  self.evaln_uri:
            raise rv.ConfigError("eval_uri is not set.")
        return ClassificationEvaluator(self.classification_uri)

    def to_proto(self):
        msg = EvaluatorConfigMsg(evaluator_type=self.transformer_type)
        if self.classification_uri:
            msg.SetField("classification_uri", self.classification_uri)
        return msg

    def builder(self):
        return ClassificationEvaluatorConfigBuilder(self)

    def preprocess_command(self, command_type, experiment_config, context=[]):
        conf = self
        if command_type == rv.ANALYZE:
            if not self.classification_uri:
                classification_uri = os.path.join(experiment_config.analyze_uri, "classification.json")
                conf = self.builder() \
                           .with_classification_uri(classification_uri) \
                           .build()
        io_def = rv.core.CommandIODefinition(output_uris=[self.classification_uri])
        return (conf, io_def)


class ClassificationEvaluatorConfigBuilder(EvaluatorConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "classification_uri": prev.classification_uri }
        super().__init__(ClassificationTransformerConfig, config)

    @staticmethod
    def from_proto(self, msg):
        b = ClassificationTransformerConfigBuilder()
        return b.with_classification_uri(msg.classification_uri)

    def with_classification_uri(self, classification_uri):
        """Set the classification_uri.

            Args:
                classification_uri: URI to the classification json to use
        """
        b = deepcopy(self)
        b.config['classification_uri'] = classification_uri
        return b

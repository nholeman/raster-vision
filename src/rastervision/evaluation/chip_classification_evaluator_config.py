from copy import deepcopy

import rastervision as rv
from rastervision.evaluation import ChipClassificationEvaluator
from rastervision.evaluation \
    import (ClassificationEvaluatorConfig, ClassificationEvaluatorConfigBuilder)
from rastervision.protos.evaluator_pb2 import EvaluatorConfig as EvaluatorConfigMsg

class ChipClassificationEvaluatorConfig(ClassificationEvaluatorConfig):
    def __init__(self, class_map, output_uri=None):
        super().__init__(rv.CHIP_CLASSIFICATION_EVALUATOR, class_map, output_uri)

    def create_evaluator(self):
        return ChipClassificationEvaluator(self.output_uri)

class ChipClassificationEvaluatorConfigBuilder(ClassificationEvaluatorConfigBuilder):
    def __init__(self, prev=None):
        super().__init__(ChipClassificationEvaluatorConfig, prev)

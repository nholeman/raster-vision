from abc import abstractmethod

from rastervision.evaluation import Evaluator

class ChipClassificationEvaluator(ClassEvaluator):
    """Evaluates predictions for a set of scenes.
    """
    def __init__(self, class_map, output_uri):
        super().__init(class_map, output_uri)

    def create_evaluator():
        return ObjectDetectionEvaluation(self.class_map)

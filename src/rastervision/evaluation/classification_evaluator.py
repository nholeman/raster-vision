from abc import (abstractmethod)

from rastervision.evaluation import Evaluator

class ChipClassificationEvaluator(Evaluator):
    """Evaluates predictions for a set of scenes.
    """
    def __init__(self, class_map, output_uri):
        self.class_map = class_map
        self.output_uri = output_uri

    @abstractmethod
    def create_evaluator():
        pass

    def process(self, scenes):
        evaluation = ChipClassificationEvaluation(self.class_map)
        for scene in scenes:
            print('Computing evaluation for scene {}...'.format(scene.scene_id))
            ground_truth = scene.ground_truth_label_source.get_labels()
            predictions = scene.prediction_label_store.get_labels()

            scene_evaluation = ChipClassificationEvaluation(self.class_map)
            scene_evaluation.compute(ground_truth, predictions)
            evaluation.merge(scene_evaluation)
        evaluation.save(self.output_uri)
from rastervision.command import Command

class EvalCommand(Command):
    def __init__(self, scenes, evaluators):
        self.scenes = scenes
        self.evaluators = evaluators

    def run(self):
        for evaluator in self.evaluators:
            evaluator.process(self.scenes)

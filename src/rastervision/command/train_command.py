from rastervision.command import Command

class TrainCommand(Command):
    def __init__(self, task):
        self.task = task

    def run(self):
        self.task.train()

from rastervision.command import Command

class ChipCommand(Command):
    def __init__(self,
                 task,
                 train_scenes,
                 val_scenes):
        self.task = task
        self.train_scenes = train_scenes
        self.val_scenes = val_scenes

    def run(self):
        self.task.make_chips(self.train_scenes,
                             self.validation_scenes)

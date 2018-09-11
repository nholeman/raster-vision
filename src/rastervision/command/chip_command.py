from rastervision.command import Command

class ChipCommand(Command):
    def __init__(self,
                 task,
                 augmentors,
                 train_scenes,
                 val_scenes):
        self.task = task
        self.augmentors = augmentors
        self.train_scenes = train_scenes
        self.val_scenes = val_scenes

    def run(self):
        self.task.make_chips(self.train_scenes,
                             self.val_scenes,
                             self.augmentors)

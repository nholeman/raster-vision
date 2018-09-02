from copy import deepcopy

class Experiment:
    def __init__(self,
                 task=None,
                 backend=None,
                 dataset=None):
        self.task = task
        self.backend = backend
        self.dataset = dataset

        self.chip_options = None

    def create_commands(self):
        if not self.chip_options:
            self.chip_options = ChipOptionsConfig.builder(self.task) \
                                                 .build()
        chip = ChipCommandConfig.builder()  \
                                .with_dataset(self.dataset) \
                                .with_options(self.chip_options) \
                                .build()
        return { rv.command.STATS: stats_config,
                 rv.command.CHIP: chip_config,
                 rv.command.TRAIN: train_config,
                 rv.command.PREDICT: predict_config,
                 rv.command.EVAL: eval_config }

    def builder():
        return ExperimentBuilder(self)

    def validate():
        pass

    @staticmethod
    def builder():
        return ExperimentBuilder()

class ExperimentBuilder():
    def __init__(self, experiment = None):
        self.experiment = experiment or Experiment()

    def with_task(self, task):
        e = deepcopy(self.experiment)
        e.task = task
        return ExperimentBuilder(e)

    def with_backend(self, backend):
        e = deepcopy(self.experiment)
        e.backend = backend
        return ExperimentBuilder(e)

    def with_dataset(self, dataset):
        e = deepcopy(self.experiment)
        e.dataset = dataset
        return ExperimentBuilder(e)

    def build(self):
        final =  deepcopy(self.experiment)
        final.validate()
        return final

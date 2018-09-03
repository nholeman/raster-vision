import os
from copy import deepcopy

import rastervision as rv
from rastervision.core.config import (Config, ConfigBuilder)
from rastervision.protos.experiment2_pb2 import ExperimentConfig2 as ExperimentConfigMsg

class ExperimentConfig(Config):
    def __init__(self,
                 name,
                 task,
                 backend,
                 dataset,
                 analyze_uri,
                 chip_uri,
                 train_uri,
                 predict_uri,
                 eval_uri):
        self.name = name
        self.task = task
        self.backend = backend
        self.dataset = dataset
        self.analyze_uri = analyze_uri
        self.chip_uri = chip_uri
        self.train_uri = train_uri
        self.predict_uri = predict_uri
        self.eval_uri = eval_uri

    # def create_commands(self):
    #     if not self.chip_options:
    #         self.chip_options = ChipOptionsConfig.builder(self.task) \
    #                                              .build()
    #     chip = ChipCommandConfig.builder()  \
    #                             .with_dataset(self.dataset) \
    #                             .with_options(self.chip_options) \
    #                             .build()
    #     return { rv.command.STATS: stats_config,
    #              rv.command.CHIP: chip_config,
    #              rv.command.TRAIN: train_config,
    #              rv.command.PREDICT: predict_config,
    #              rv.command.EVAL: eval_config }

    def to_proto(self):
        msg = ExperimentConfigMsg(name=self.name,
                                  task=self.task.to_proto(),
                                  backend=self.backend.to_proto(),
                                  dataset=self.dataset.to_proto())
        msg.analyze_uri = self.analyze_uri
        msg.chip_uri = self.chip_uri
        msg.train_uri = self.train_uri
        msg.predict_uri = self.predict_uri
        msg.eval_uri = self.eval_uri
        return msg

    def builder():
        return ExperimentConfigBuilder(self)

    @staticmethod
    def builder():
        return ExperimentConfigBuilder()

    @staticmethod
    def from_proto(msg):
        """Creates an ExperimentConfig from the specificed protobuf message
        """
        return ExperimentConfigBuilder().from_proto(msg).build()

class ExperimentConfigBuilder(ConfigBuilder):
    def __init__(self, prev = None):
        config = {}
        if prev:
            config = { "name": prev.name,
                       "task": prev.task,
                       "backend": prev.backend,
                       "dataset": prev.dataset,
                       "analyze_uri": prev.analyze_uri,
                       "chip_uri": prev.chip_uri,
                       "train_uri": prev.train_uri,
                       "predict_uri": prev.predict_uri,
                       "eval_uri": prev.eval_uri }
        super().__init__(ExperimentConfig, config)
        self.root_uri = None
        self.analyze_key = "default"
        self.chip_key = "default"
        self.train_key = "default"
        self.predict_key = "default"
        self.eval_key = "default"

    def build(self):
        self.validate()
        # Build any missing paths through
        b = self
        if not self.config.get('analyze_uri'):
            if not self.root_uri:
                raise rv.ConfigError("Need to set root_uri if command uri's not explicitly set.")
            uri = os.path.join(self.root_uri, rv.ANALYZE.lower(), self.analyze_key)
            b = b.with_analyze_uri(uri)
        if not self.config.get('chip_uri'):
            if not self.root_uri:
                raise rv.ConfigError("Need to set root_uri if command uri's not explicitly set.")
            uri = os.path.join(self.root_uri, rv.CHIP.lower(), self.chip_key)
            b = b.with_chip_uri(uri)
        if not self.config.get('train_uri'):
            if not self.root_uri:
                raise rv.ConfigError("Need to set root_uri if command uri's not explicitly set.")
            uri = os.path.join(self.root_uri, rv.TRAIN.lower(), self.train_key)
            b = b.with_train_uri(uri)
        if not self.config.get('predict_uri'):
            if not self.root_uri:
                raise rv.ConfigError("Need to set root_uri if command uri's not explicitly set.")
            uri = os.path.join(self.root_uri, rv.PREDICT.lower(), self.predict_key)
            b = b.with_predict_uri(uri)
        if not self.config.get('eval_uri'):
            if not self.root_uri:
                raise rv.ConfigError("Need to set root_uri if command uri's not explicitly set.")
            uri = os.path.join(self.root_uri, rv.EVAL.lower(), self.eval_key)
            b = b.with_eval_uri(uri)

        return ExperimentConfig(**b.config)

    def from_proto(self, msg):
        b = ExperimentConfigBuilder()
        return b.with_name(msg.name) \
                .with_task(rv.TaskConfig.from_proto(msg.task)) \
                .with_backend(rv.BackendConfig.from_proto(msg.backend)) \
                .with_dataset(rv.DatasetConfig.from_proto(msg.dataset)) \
                .with_analyze_uri(msg.analyze_uri) \
                .with_chip_uri(msg.analyze_uri) \
                .with_train_uri(msg.analyze_uri) \
                .with_predict_uri(msg.analyze_uri) \
                .with_eval_uri(msg.analyze_uri)

    def with_name(self, name):
        b = deepcopy(self)
        b.config['name'] = name
        return b

    def with_task(self, task):
        b = deepcopy(self)
        b.config['task'] = task
        return b

    def with_backend(self, backend):
        b = deepcopy(self)
        b.config['backend'] = backend
        return b

    def with_dataset(self, dataset):
        b = deepcopy(self)
        b.config['dataset'] = dataset
        return b

    def with_analyze_uri(self, uri):
        b = deepcopy(self)
        b.config['analyze_uri'] = uri
        return b

    def with_chip_uri(self, uri):
        b = deepcopy(self)
        b.config['chip_uri'] = uri
        return b

    def with_train_uri(self, uri):
        b = deepcopy(self)
        b.config['train_uri'] = uri
        return b

    def with_predict_uri(self, uri):
        b = deepcopy(self)
        b.config['predict_uri'] = uri
        return b

    def with_eval_uri(self, uri):
        b = deepcopy(self)
        b.config['eval_uri'] = uri
        return b

    def with_root_uri(self, uri):
        b = deepcopy(self)
        b.root_uri = uri
        return b

    def with_analyze_key(self, key):
        b = deepcopy(self)
        b.analyze_key = key
        return b

    def with_chip_key(self, key):
        b = deepcopy(self)
        b.chip_key = key
        return b

    def with_train_key(self, key):
        b = deepcopy(self)
        b.train_key = key
        return b

    def with_predict_key(self, key):
        b = deepcopy(self)
        b.predict_key = key
        return b

    def with_eval_key(self, key):
        b = deepcopy(self)
        b.eval_key = key
        return b

from abc import abstractmethod
from copy import deepcopy
import os
import json

import rastervision as rv
from rastervision.core import (Config, ConfigBuilder)
from rastervision.utils.files import file_exists

class BackendConfig(Config):
    class TrainOptions:
        def __init__(self,
                     sync_interval=600,
                     do_monitoring=True,
                     replace_model=False):
            self.sync_interval = sync_interval
            self.do_monitoring = do_monitoring
            self.replace_model = replace_model

    def __init__(self,
                 backend_type,
                 pretrained_model_uri=None,
                 train_options=TrainOptions()):
        self.backend_type = backend_type
        self.pretrained_model_uri = pretrained_model_uri
        self.train_options = train_options

    @abstractmethod
    def create_backend(self, task_config):
        """Create the Backend that this configuration represents

           Args:
              task_config: The task configuration for the task
                           to be accomplished by this backend.
        """
        pass

    @staticmethod
    def builder(backend_type):
        return rv._registry.get_config_builder(rv.BACKEND, backend_type)()

    @staticmethod
    def from_proto(msg):
        """Creates a BackendConfig from the specificed protobuf message
        """
        return rv._registry.get_config_builder(rv.BACKEND, msg.backend_type)() \
                           .from_proto(msg) \
                           .build()

class BackendConfigBuilder(ConfigBuilder):
    def __init__(self, backend_type, config_class, config={}, prev=None):
        if prev:
            config['train_options'] = prev.train_options
        super().__init__(config_class, config)
        self.task = None
        self.backend_type = backend_type

    @abstractmethod
    def _applicable_tasks(self):
        """Returns the tasks that this backend can be applied to.
        """
        pass

    @abstractmethod
    def _process_task(self, task):
        """Subclasses override this to set up configuration related
           to this task
        """
        pass

    def from_proto(self, msg):
        return self.with_train_options(
            sync_interval=msg.train_options.sync_interval,
            do_monitoring=msg.train_options.do_monitoring,
            replace_model=msg.train_options.replace_model)


    def with_task(self, task):
        """Sets the backend up for a specific task type, e.g. rv.OBJECT_DETECTION.
        """
        if not task.task_type in self._applicable_tasks():
            raise Exception(
                "Backend of type {} cannot be applied to task type {}" \
                .format(task.task_type, self.config.backend_type))
        b = deepcopy(self)
        b.task = task
        b = b._process_task()
        return b

    def with_pretrained_model(self, uri):
        """Set a pretrained model URI. The filetype and meaning
           for this model will be different based on the backend implementation.
        """
        b = deepcopy(self)
        b.config['pretrained_model_uri'] = uri
        return b

    def with_train_options(self,
                           sync_interval=600,
                           do_monitoring=True,
                           replace_model=False):
        """Sets the train options for this backend.

           Args:
              sync_interval: How often to sync output of training to the cloud (in seconds).

              do_monitoring: Run process to monitor training (eg. Tensorboard)

              replace_model: Replace the model checkpoint if exists.
                             If false, this will continue training from checkpoing if exists,
                             if the backend allows for this.
        """
        b = deepcopy(self)
        b.config['train_options'] = BackendConfig.TrainOptions(sync_interval,
                                                               do_monitoring,
                                                               replace_model)
        return b

    # TODO: Allow client configuration of model defaults.
    # This should be purely client side. Allow for this to be set
    # in ~/.rastervision configuration.
    def with_model_defaults(self, model_defaults_key):
        """Sets the backend configuration and pretrained model defaults
           according to the model defaults configuraiton
          (see model_defaults.json in this package)
        """
        model_defaults  = {}
        model_defaults_path = os.path.join(os.path.dirname(__file__), "model_defaults.json")
        with open(model_defaults_path) as f:
            model_defaults = json.loads(f.read())

        if self.backend_type in model_defaults:
            backend_defaults = model_defaults[self.backend_type]
            if model_defaults_key in backend_defaults:
                return self._load_model_defaults(backend_defaults[model_defaults_key])
            else:
                raise rv.ConfigError("No defaults found for model key {}" \
                                     .format(model_defaults_key))
        else:
            raise rv.ConfigError("No model defaults for backend {}" \
                                 .format(self.backend_type))
        return self

    def _load_model_defaults(self, model_defaults):
        """Overriding classes should handle this if they
           want to allow default parameters to be loaded
           from the default configurations.
        """
        return self

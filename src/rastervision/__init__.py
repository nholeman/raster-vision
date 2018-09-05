from rastervision.protos.model_config_pb2 import ModelConfig

from rastervision.core import ConfigError
from rastervision.analyzer.api import *
from rastervision.backend.api import *
from rastervision.command.api import *
from rastervision.data.api import *
from rastervision.experiment.api import  *
from rastervision.task.api import *

# TODO: Is this necessary? numpy does it.
#__all__ = ["Experiment"]
# __all__.extend(task.api.__all__)
# __all__.extend(backend.api.__all__)

from .registry import Registry

_registry = None

def _initialize():
    global _registry

    if not _registry:
        _registry = Registry()

_initialize()

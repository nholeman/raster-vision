from rastervision.protos.model_config_pb2 import ModelConfig

__all__ = ["Experiment"]

from .core import ConfigError
from .experiment import  *
from .task import *
from .backend import *
from rastervision.data.api import *

# TODO: Is this necessary? numpy does it.
# __all__.extend(task.__all__)
# __all__.extend(backend.__all__)

from .registry import Registry

_registry = None

def _initialize():
    global _registry

    if not _registry:
        _registry = Registry()

_initialize()

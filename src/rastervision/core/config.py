from abc import (ABC, abstractmethod)
from copy import deepcopy

class ConfigError(Exception):
    pass

def set_nested_keys(target, mods, ignore_missing_keys):
    """Sets dictionary keys based on modifications stated
       in a dictionary. TODO: Explain.
       Only overrides values, does not replace dicts.
       TODO: Errors will be user facing, so provide good feedback.
    """
    searched_keys, found_keys = [], []

    def f(_target, _mods):
        for key in _target:
            if key in _mods.keys():
                found_keys.append(key)
                if type(_target[key]) is dict:
                    if type(_mods[key]) is dict:
                        f(_target[key], _mods[key])
                    else:
                        raise ConfigError("Error: cannot modify dict with value")
                else:
                    _target[key] = _mods[key]
            else:
                if type(_target[key]) is dict:
                    f(_target[key], _mods)
        searched_keys.extend(list(_mods.keys()))

    f(target, mods)
    if not ignore_missing_keys:
        d = set(searched_keys) - set(found_keys)
        if d:
            raise ConfigError("Mod keys not found in target dict: {}".format(d))


class Config(ABC):
    @abstractmethod
    def builder(self):
        """Return a builder based on this config.
        """
        pass

    @abstractmethod
    def to_proto(self):
        """Returns the protobuf configuration for this config.
        """
        pass

    @staticmethod
    @abstractmethod
    def builder():
        """Returns a new builder that takes this configuration
           as its starting point.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_proto(msg):
        """Creates a Config from the specificed protobuf message
        """
        pass

class ConfigBuilder(ABC):
    def __init__(self, config_class, config={}):
        """Construct a builder.

           Args:
             config_class: The Config class that this builder builds.
             config: A dictionary of **kwargs that will eventually be passed
                     into the __init__ method of config_class to build the configuration.
                     This config is modified with the fluent builder methods.
        """
        self.config_class = config_class
        self.config = config

    def build(self):
        """Returns the configuration that is built by this builder.
        """
        self.validate()
        return self.config_class(**self.config)

    def validate(self):
        """Validate this config, if there is validation on the builder that
           is not captured by the required arguments of the config.
        """
        pass

    @abstractmethod
    def from_proto(self, msg):
        """Return a builder that takes the configuration from the proto message
           as its starting point.
        """
        pass

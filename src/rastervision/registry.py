import rastervision as rv
from rastervision.task.object_detection_config import ObjectDetectionConfigBuilder
from rastervision.task.chip_classification_config import ChipClassificationConfigBuilder
from rastervision.backend.tf_object_detection_config import TFObjectDetectionConfigBuilder
from rastervision.data.raster_transformer.channel_transformer_config \
    import ChannelTransformerConfigBuilder
from rastervision.data.raster_transformer.stats_transformer_config \
    import StatsTransformerConfigBuilder
from rastervision.data.raster_source.default import (DefaultGeoTiffSourceProvider,
                                                     DefaultImageSourceProvider)
from rastervision.data.label_source.default import (DefaultObjectDetectionGeoJSONSourceProvider,
                                                    DefaultChipClassificationGeoJSONSourceProvider)
from rastervision.data.label_store.default import (DefaultObjectDetectionGeoJSONStoreProvider,
                                                   DefaultChipClassificationGeoJSONStoreProvider)
from rastervision.protos.task_pb2 import TaskConfig

class RegistryError(Exception):
    pass

class Registry:
    """Singleton that holds instances of Raster Vision types,
       to be referenced by configuration code by key.
    """

    def __init__(self):
        self._internal_config_builders =  {
            # Tasks
            (rv.TASK, rv.OBJECT_DETECTION): ObjectDetectionConfigBuilder,
            (rv.TASK, rv.CHIP_CLASSIFICATION): ChipClassificationConfigBuilder,

            # Backends
            (rv.BACKEND, rv.TF_OBJECT_DETECTION): TFObjectDetectionConfigBuilder,

            # Raster Transformers
            (rv.RASTER_TRANSFORMER, rv.STATS_TRANSFORMER): StatsTransformerConfigBuilder,

            # Raster Sources
            (rv.RASTER_SOURCE, rv.GEOTIFF_SOURCE): rv.data.GeoTiffSourceConfigBuilder,
            (rv.RASTER_SOURCE, rv.IMAGE_SOURCE): rv.data.ImageSourceConfigBuilder,

            # Label Sources
            (rv.LABEL_SOURCE,
             rv.OBJECT_DETECTION_GEOJSON): rv.data.ObjectDetectionGeoJSONSourceConfigBuilder,
            # (rv.LABEL_SOURCE,
            #  rv.CHIP_CLASSIFICATION_GEOJSON): rv.data.ChipClassificationGeoJSONSourceConfigBuilder,
        }

        self._internal_raster_sources = [
            DefaultGeoTiffSourceProvider,
            # This is the catch-all case, ensure it's on the bottom of the search stack.
            DefaultImageSourceProvider
        ]

        self._internal_label_sources = [
            DefaultObjectDetectionGeoJSONSourceProvider,
            DefaultChipClassificationGeoJSONSourceProvider
        ]

        self._internal_label_stores = [
            DefaultObjectDetectionGeoJSONStoreProvider,
            DefaultChipClassificationGeoJSONStoreProvider
        ]

        self.command_config_builders = {
            rv.ANALYZE: rv.command.AnalyzeCommandConfigBuilder,
            rv.CHIP: rv.command.ChipCommandConfigBuilder,
            rv.TRAIN: rv.command.TrainCommandConfigBuilder,
            rv.PREDICT: rv.command.PredictCommandConfigBuilder,
            rv.EVAL: rv.command.EvalCommandConfigBuilder
        }

        self.experiment_runners = {
            rv.LOCAL_RUNNER: rv.runner.LocalExperimentRunner
        }

    def get_config_builder(self, group, key):
        internal_builder = self._internal_config_builders.get((group, key))
        if internal_builder:
            return internal_builder
        else:
            # TODO: Search plugins
            pass

        raise RegistryError("Unknown type {} for {} ".format(key, group))

    def get_default_raster_source_provider(self, s):
        """
        Gets the DefaultRasterSourceProvider for a given input string.
        """
        for provider in self._internal_raster_sources:
            if provider.handles(s):
                return provider

        # TODO: Search plugins

        raise RegistryError("No DefaultRasterSourceProvider found for {}".format(s))

    def get_default_label_source_provider(self, task_type, s):
        """
        Gets the DefaultRasterSourceProvider for a given input string.
        """
        for provider in self._internal_label_sources:
            if provider.handles(task_type, s):
                return provider

        # TODO: Search plugins

        raise RegistryError("No DefaultLabelSourceProvider "
                            "found for {} and task type {}".format(s, task_type))

    def get_default_label_store_provider(self, task_type, s=None):
        """
        Gets the DefaultRasterSourceProvider for a given input string.
        """
        for provider in self._internal_label_sources:
            if s:
                if provider.handles(task_type, s):
                    return provider
            else:
                if provider.is_default_for(task_type):
                    return provider

        # TODO: Search plugins

        raise RegistryError("No DefaultLabelStoreProvider "
                            "found for {} and task type {}".format(s, task_type))

    def get_command_config_builder(self, command_type):
        builder = self.command_config_builder.get(command_type)
        if not builder:
            raise RegistryError("No command found for type {}".format(command_type))
        return builder

    def get_experiment_runner(self, runner_type):
        runner = self.experiment_runners.get(runner_type)
        if not runner:
            # TODO: Search plugins
            raise RegistryError("No experiment runner for type {}".format(runner_type))

        return experiment_runner

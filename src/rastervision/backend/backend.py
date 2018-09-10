from abc import ABC, abstractmethod


class Backend(ABC):
    """Functionality for a specific implementation of an MLTask.

    This should be subclassed to provide a bridge to third party ML libraries.
    There is a many-to-one relationship from backends to tasks.
    """

    @abstractmethod
    def process_scene_data(self, scene, data, class_map, options):
        """Process each scene's training data

        Args:
            scene: Scene
            data: TrainingData
            class_map: ClassMap
            options: MakeChipsConfig.Options

        Returns:
            backend-specific data-structures consumed by ml_backend's
            process_sceneset_results
        """
        pass

    @abstractmethod
    def process_sceneset_results(self, training_results, validation_results,
                                 class_map, options):
        """After all scenes have been processed, process the resultset

        Args:
            training_results: dependent on the ml_backend's process_scene_data
            validation_results: dependent on the ml_backend's
                process_scene_data
            class_map: ClassMap
            options: MakeChipsConfig.Options
        """
        pass

    @abstractmethod
    def train(self, options):
        """Train a model.

        Args:
            options: TrainConfig.Options
        """
        pass

    @abstractmethod
    def predict(self, chips, windows, options):
        """Return predictions for a chip using model.

        Args:
            chips: [[height, width, channels], ...] numpy array of chips
            windows: List of boxes that are the windows aligned with the chips.
            options: PredictConfig.Options
        """
        pass
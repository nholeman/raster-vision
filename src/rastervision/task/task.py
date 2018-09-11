from abc import abstractmethod

import numpy as np

from rastervision.core.training_data import TrainingData
from rastervision.core.predict_package import save_predict_package
from rastervision.data import ObjectDetectionLabels

# TODO: DRY... same keys as in ml_backends/tf_object_detection_api.py
TRAIN = 'train'
VALIDATION = 'validation'


class Task(object):
    """Functionality for a specific machine learning task.

    This should be subclassed to add a new task, such as object detection
    """

    def __init__(self, task_config, backend):
        """Construct a new Task.

        Args:
            task_config: TaskConfig
            backend: Backend
        """
        self.config = task_config
        self.backend = backend

    @abstractmethod
    def get_train_windows(self, scene):
        """Return the training windows for a Scene.

        The training windows represent the spatial extent of the training
        chips to generate.

        Args:
            scene: Scene to generate windows for

        Returns:
            list of Boxes
        """
        pass

    @abstractmethod
    def get_train_labels(self, window, scene):
        """Return the training labels in a window for a scene.

        Args:
            window: Box
            scene: Scene

        Returns:
            Labels that lie within window
        """
        pass

    @abstractmethod
    def post_process_predictions(self, labels):
        """Runs a post-processing step on labels at end of prediction.

        Returns:
            Labels
        """
        pass

    @abstractmethod
    def get_predict_windows(self, extent):
        """Return windows to compute predictions for.

        Args:
            extent: Box representing extent of RasterSource

        Returns:
            list of Boxes
        """
        pass

    @abstractmethod
    def get_evaluation(self):
        """Return empty Evaluation of appropriate type.

        This functions as a factory.
        """
        pass

    @abstractmethod
    def save_debug_predict_image(self, scene, debug_dir_uri):
        """Save a debug image of predictions.

        This writes to debug_dir_uri/<scene.id>.jpg.
        """
        pass

    def make_chips(self, train_scenes, validation_scenes, augmentors):
        """Make training chips.

        Convert Scenes with a ground_truth_label_store into training
        chips in MLBackend-specific format, and write to URI specified in
        options.

        Args:
            train_scenes: list of Scene
            validation_scenes: list of Scene
                (that is disjoint from train_scenes)
            augmentors: Augmentors used to augment training data
        """

        def _process_scene(scene, type_, augment):
            data = TrainingData()
            print(
                'Making {} chips for scene: {}'.format(type_, scene.scene_id),
                end='',
                flush=True)
            windows = self.get_train_windows(scene)
            for window in windows:
                chip = scene.raster_source.get_chip(window)
                labels = self.get_train_labels(window, scene)
                data.append(chip, window, labels)
                print('.', end='', flush=True)
            print()
            # Shuffle data so the first N samples which are displayed in
            # Tensorboard are more diverse.
            data.shuffle()

            # Process augmentation
            if augment:
                for augmentor in augmentors:
                    data = augmentor.process(data)

            return self.backend.process_scene_data(scene, data)

        def _process_scenes(scenes, type_, augment):
            return [_process_scene(scene, type_, augment) for scene in scenes]

        # TODO: parallel processing!
        processed_training_results = _process_scenes(train_scenes,
                                                     TRAIN,
                                                     augment=True)
        processed_validation_results = _process_scenes(validation_scenes,
                                                       VALIDATION,
                                                       augment=False)

        self.backend.process_sceneset_results(processed_training_results,
                                              processed_validation_results)

    def train(self):
        """Train a model.
        """
        self.backend.train()

    def predict(self, scenes):
        """Make predictions for scenes.

        The predictions are saved to the prediction_label_store in
        each scene.

        Args:
            scenes: list of Scenes
        """

        for scene in scenes:
            print('Making predictions for scene', end='', flush=True)
            raster_source = scene.raster_source
            label_store = scene.prediction_label_store

            labels = ObjectDetectionLabels.make_empty()

            windows = self.get_predict_windows(raster_source.get_extent())

            def predict_batch(predict_chips, predict_windows):
                new_labels = self.backend.predict(
                    np.array(predict_chips), predict_windows)
                labels = ObjectDetectionLabels.concatenate(labels, new_labels)
                print('.' * len(predict_chips), end='', flush=True)

            batch_chips, batch_windows = [], []
            for window in windows:
                chip = raster_source.get_chip(window)
                if np.any(chip):
                    batch_chips.append(chip)
                    batch_windows.append(window)

                # Predict on batch
                if len(batch_chips) >= self.config.predict_batch_size:
                    predict_batch(batch_chips, batch_windows)
                    batch_chips, batch_windows = [], []

            # Predict on remaining batch
            if len(batch_chips) > 0:
                predict_batch(batch_chips, batch_windows)

            print()

            labels = self.post_process_predictions(labels)
            label_store.save(labels)

            # TODO: Debug?
            # if (options.debug and options.debug_uri
            #         and self.class_map.has_all_colors()):
            #     self.save_debug_predict_image(scene, options.debug_uri)

            # TODO: Predict Package
            # if options.prediction_package_uri:
            #     save_predict_package(config)

    # def eval(self, scenes, options):
    #     """Evaluate predictions against ground truth in scenes.

    #     Writes output to URI in options.

    #     Args:
    #         scenes: list of Scenes that contain both
    #             ground_truth_label_store and prediction_label_store
    #         options: EvalConfig.Options
    #     """
    #     evaluation = self.get_evaluation()
    #     for scene in scenes:
    #         print('Computing evaluation for scene {}...'.format(scene.scene_id))
    #         ground_truth = scene.ground_truth_label_source.get_labels()
    #         predictions = scene.prediction_label_store.get_labels()

    #         scene_evaluation = self.get_evaluation()
    #         scene_evaluation.compute(ground_truth, predictions)
    #         evaluation.merge(scene_evaluation)
    #     evaluation.save(options.output_uri)

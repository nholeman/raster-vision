from copy import deepcopy

import rastervision as rv
from .task_config import (TaskConfig, TaskConfigBuilder)
from .util import (construct_classes, classes_to_class_items)
from ..protos.task_pb2 import TaskConfig as TaskConfigMsg

class ObjectDetectionConfig(TaskConfig):
    def __init__(self,
                 classes={},
                 chip_size=300):
        super().__init__(rv.OBJECT_DETECTION)
        self.classes = classes
        self.chip_size = chip_size

    def create_task(self, backend):
        return rv.ml_task.ObjectDetection(backend, self)

    def builder(self):
        return ObjectDetectionConfigBuilder(self)

    def to_proto(self):
        conf = TaskConfigMsg.ObjectDetectionConfig(chip_size=self.chip_size,
                                                   class_items=classes_to_class_items(self.classes))
        return TaskConfigMsg(task_type=rv.OBJECT_DETECTION,
                             object_detection_config=conf)

class ObjectDetectionConfigBuilder(TaskConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = { "classes": classes,
                       "chip_size": chip_size }
        super().__init__(ObjectDetectionConfig, config)

    def from_proto(self, msg):
        conf = msg.object_detection_config
        b = ObjectDetectionConfigBuilder()
        return b.with_classes(conf.class_items) \
                .with_chip_size(conf.chip_size)

    def with_classes(self, classes):
        """Set the classes for this task.

            Args:
                classes: Either a list of class names, a dict which
                         maps class names to class ids, or a dict
                         which maps class names to a tuple of (class_id, color),
                         where color is a PIL color string.
        """
        b = deepcopy(self)
        b.config['classes'] = construct_classes(classes)
        return b

    def with_chip_size(self, chip_size):
        """Set the chip_size for this task.

            Args:
                chip_size: Integer value chip size
        """
        b = deepcopy(self)
        b.config['chip_size'] = chip_size
        return b

import numpy as np

from object_detection.utils.np_box_list import BoxList
from object_detection.utils.np_box_list_ops import (
    prune_non_overlapping_boxes, clip_to_window, concatenate,
    non_max_suppression)

from rastervision.core.box import Box
from rastervision.core.labels import Labels


class ObjectDetectionLabels(Labels):
    """A set of boxes and associated class_ids and scores.

    Implemented using the Tensorflow Object Detection API's BoxList class.
    """

    def __init__(self, npboxes, class_ids, scores=None):
        """Construct a set of object detection labels.

        Args:
            npboxes: float numpy array of size nx4 with cols
                ymin, xmin, ymax, xmax. Should be in pixel coordinates within
                the global frame of reference.
            class_ids: int numpy array of size n with class ids starting at 1
            scores: float numpy array of size n
        """
        self.boxlist = BoxList(npboxes)
        # This field name actually needs to be 'classes' to be able to use
        # certain utility functions in the TF Object Detection API.
        self.boxlist.add_field('classes', class_ids)
        # We need to ensure that there is always a scores field so that the
        # concatenate method will work with empty labels objects.
        if scores is None:
            scores = np.ones(class_ids.shape)
        self.boxlist.add_field('scores', scores)

    def assert_equal(self, expected_labels):
        np.testing.assert_array_equal(self.get_npboxes(),
                                      expected_labels.get_npboxes())
        np.testing.assert_array_equal(self.get_class_ids(),
                                      expected_labels.get_class_ids())
        np.testing.assert_array_equal(self.get_scores(),
                                      expected_labels.get_scores())

    @staticmethod
    def make_empty():
        npboxes = np.empty((0, 4))
        class_ids = np.empty((0, ))
        scores = np.empty((0, ))
        return ObjectDetectionLabels(npboxes, class_ids, scores)

    @staticmethod
    def from_boxlist(boxlist):
        """Make ObjectDetectionLabels from BoxList object."""
        scores = (boxlist.get_field('scores')
                  if boxlist.has_field('scores') else None)
        return ObjectDetectionLabels(
            boxlist.get(), boxlist.get_field('classes'), scores=scores)

    def get_boxes(self):
        """Return list of Boxes."""
        return [Box.from_npbox(npbox) for npbox in self.boxlist.get()]

    def get_npboxes(self):
        return self.boxlist.get()

    def get_scores(self):
        if self.boxlist.has_field('scores'):
            return self.boxlist.get_field('scores')
        return None

    def get_class_ids(self):
        return self.boxlist.get_field('classes')

    def __len__(self):
        return self.boxlist.get().shape[0]

    def __str__(self):
        return str(self.boxlist.get())

    def to_boxlist(self):
        return self.boxlist

    @staticmethod
    def local_to_global(npboxes, window):
        """Convert from local to global coordinates.

        The local coordinates are row/col within the window frame of reference.
        The global coordinates are row/col within the extent of a RasterSource.
        """
        xmin = window.xmin
        ymin = window.ymin
        return npboxes + np.array([[ymin, xmin, ymin, xmin]])

    @staticmethod
    def global_to_local(npboxes, window):
        """Convert from global to local coordinates.

        The global coordinates are row/col within the extent of a RasterSource.
        The local coordinates are row/col within the window frame of reference.
        """
        xmin = window.xmin
        ymin = window.ymin
        return npboxes - np.array([[ymin, xmin, ymin, xmin]])

    @staticmethod
    def local_to_normalized(npboxes, window):
        """Convert from local to normalized coordinates.

        The local coordinates are row/col within the window frame of reference.
        Normalized coordinates range from 0 to 1 on each (height/width) axis.
        """
        height = window.get_height()
        width = window.get_width()
        return npboxes / np.array([[height, width, height, width]])

    @staticmethod
    def normalized_to_local(npboxes, window):
        """Convert from normalized to local coordinates.

        Normalized coordinates range from 0 to 1 on each (height/width) axis.
        The local coordinates are row/col within the window frame of reference.
        """
        height = window.get_height()
        width = window.get_width()
        return npboxes * np.array([[height, width, height, width]])

    @staticmethod
    def get_overlapping(labels, window, ioa_thresh=0.000001, clip=False):
        """Return subset of labels that overlap with window.

        Args:
            labels: ObjectDetectionLabels
            window: Box
            ioa_thresh: the minimum IOA for a box to be considered as
                overlapping
            clip: if True, clip label boxes to the window
        """
        window_npbox = window.npbox_format()
        window_boxlist = BoxList(np.expand_dims(window_npbox, axis=0))
        boxlist = prune_non_overlapping_boxes(
            labels.boxlist, window_boxlist, minoverlap=ioa_thresh)
        if clip:
            boxlist = clip_to_window(boxlist, window_npbox)

        return ObjectDetectionLabels.from_boxlist(boxlist)

    @staticmethod
    def concatenate(labels1, labels2):
        """Return concatenation of labels.

        Args:
            labels1: ObjectDetectionLabels
            labels2: ObjectDetectionLabels
        """
        new_boxlist = concatenate([labels1.to_boxlist(), labels2.to_boxlist()])
        return ObjectDetectionLabels.from_boxlist(new_boxlist)

    @staticmethod
    def prune_duplicates(labels, score_thresh, merge_thresh):
        """Remove duplicate boxes.

        Runs non-maximum suppression to remove duplicate boxes that result from
        sliding window prediction algorithm.

        Args:
            labels: ObjectDetectionLabels
            score_thresh: the minimum allowed score of boxes
            merge_thresh: the minimum IOA allowed when merging two boxes
                together

        Returns:
            ObjectDetectionLabels
        """
        max_output_size = 1000000
        pruned_boxlist = non_max_suppression(
            labels.boxlist,
            max_output_size=max_output_size,
            iou_threshold=merge_thresh,
            score_threshold=score_thresh)
        return ObjectDetectionLabels.from_boxlist(pruned_boxlist)

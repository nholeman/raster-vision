import json

from rastervision.data.label_store import LabelStore
from rastervision.data.label_store.utils import boxes_to_geojson
from rastervision.utils.files import str_to_file


class ObjectDetectionGeoJSONStore(LabelStore):
    def __init__(self,
                 uri,
                 crs_transformer,
                 class_map):
        """Construct LabelStore backed by a GeoJSON file for object detection labels.

        Args:
            uri: uri of GeoJSON file containing labels
            crs_transformer: CRSTransformer to convert from map coords in label
                in GeoJSON file to pixel coords.
            class_map: ClassMap used to infer class_ids from class_name
                (or label) field
        """
        self.uri = uri
        self.crs_transformer = crs_transformer
        self.class_map = class_map

    def save(self, labels):
        """Save labels to URI."""
        boxes = labels.get_boxes()
        class_ids = labels.get_class_ids().tolist()
        scores = labels.get_scores().tolist()
        geojson_dict = boxes_to_geojson(
            boxes,
            class_ids,
            self.crs_transformer,
            self.class_map,
            scores=scores)
        geojson_str = json.dumps(geojson_dict)
        str_to_file(geojson_str, self.uri)

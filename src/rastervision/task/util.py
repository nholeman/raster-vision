from ..protos.task_pb2 import TaskConfig

def construct_classes(classes):
    """Construct the cononical set of classes from a number of different
       representations.

       The cononical class representation is a dict that makes class names
       to an ID and an optional color string, e.g.:
       TODO - how to format code in pydocs
       {
           "car": (1, Red),
           "misc": (2, None)
       }

        Args:
            classes: One of the following:
                     - a list of class names
                     - a list of ClassItem protobuf messages
                     - a dict which maps class names to class ids
                     - a dict which maps class names to a tuple of
                       (class_id, color), where color is a PIL color string.
    """
    result = {}
    if type(classes) is dict:
        if not len(classes.items()) == 0:
            if type(classes.items()[0]) is tuple:
                # This dict already has colors mapped to class ids
                result = classes
            else:
                # Map items to empty colors
                for k, v in classes:
                    result[k] = (v, "")
    else:
        if not len(classes) == 0:
            if type(classes[0]) is TaskConfig.ClassItem:
                for item in  classes:
                    result[item.name] = (item.id, item.color)
            else:
                for i, name in enumerate(classes):
                    result[name] = (i, None)

    return result

def classes_to_class_items(classes):
    """Transform the cononcal representation of classes into
       a list of ClassItem protobuf messages
    """

    return [TaskConfig.ClassItem(name=name, id=class_id, color=color)
            for name, (class_id, color) in classes.items()]

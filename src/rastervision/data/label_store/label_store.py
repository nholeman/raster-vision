from abc import ABC, abstractmethod


class LabelStore(ABC):
    """This defines how to store prediction labels are stored for a scene.
    """

    @abstractmethod
    def save(self, labels):
        """Save.

        Args:
           labels - Labels to be saved, the type of which will be dependant on the type
                    of task.
        """
        pass

    @abstractmethod
    def load(self):
        """Loads Labels from this label store."""
        pass

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def run(self):
        """Run the command."""
        pass

class NoOpCommand(Command):
    """Defines a command that does nothing.
    """
    def run(self):
        pass

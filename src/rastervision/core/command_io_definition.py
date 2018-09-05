
class CommandIODefinition:
    """Class which contains a set of inputs and outputs for a command,
       based on the configuration.
    """
    def __init__(self,
                 input_uris=[],
                 output_uris=[],
                 missing_input_messages=[]):
        self.input_uris = []
        self.output_uris = []

        # Messages that declare missing inputs
        self.missing_input_messages = []

    def merge(self, other):
        self.input_uris = self.input_uris + other.input_uris
        self.output_uris = self.output_uris + other.output_uris
        self.missing_input_messages = self.mssing_input_messages + \
                                      other.missing_input_messages

    def add_input(self, input_uri):
        self.input_uris.append(input_uri)

    def add_inputs(self, input_uris):
        self.input_uris.extend(input_uris)

    def add_output(self, output_uri):
        self.output_uri.append(output_uri)

    def add_outputs(self, output_uri):
        self.output_uri.extend(output_uris)

    def add_missing(self, message):
        self.missing_input_messages.append(message)

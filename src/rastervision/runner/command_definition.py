from typing import List

import rastervision as rv

class CommandDefinition:
    def __init__(self, experiment_id, command_config, io_def):
        self.experiment_id = experiment_id
        self.command_config = command_config
        self.io_def = io_def

    @classmethod
    def from_experiments(cls, experiments: List[rv.ExperimentConfig]):
        command_definitions = []

        for experiment in experiments:
            e = experiment
            command_definitions = []
            for command_type in rv.ALL_COMMANDS:
                print("PROCESSING COMMAND {}".format(command_type))
                (e, io_def) = e.preprocess_command(command_type, e)
                print("INPUTS:")
                for i in io_def.input_uris:
                    print("\t{}".format(i))
                print("OUTPUTS:")
                for i in io_def.output_uris:
                    print("\t{}".format(i))
                command_config = e.make_command_config(command_type)
                command_def = cls(e.id, command_config, io_def)
                command_definitions.append(command_def)

        return command_definitions

    @staticmethod
    def filter_commands(command_definitions, target_commands):
        """Filters commands by the target command type."""
        return list(
            filter(lambda c: c.command_config.command_type in target_commands,
                   command_definitions))

    @staticmethod
    def remove_duplicates(command_definitions):
        """Remove duplicate commands.

        Removes duplicated commands, defining equality for a command by
        the tuple (command_type, input_uris, output_uris)
        """

        unique_commands = []
        seen_commands = set([])
        for command_def in command_definitions:
            k = (command_def.command_config.command_type,
                 '|'.join(sorted(command_def.io_def.input_uris)),
                 '|'.join(sorted(command_def.io_def.output_uris)))
            if not k in seen_commands:
                seen_commands.add(k)
                unique_commands.append(command_def)

        return unique_commands

    @staticmethod
    def get_missing_inputs(command_definitions):
        """Gathers missing inputs from a set of commands.

        Returns a dictionary of experiment id to list of missing input URIs.
        """
        missing_inputs = {}
        for command_def in command_definitions:
            if command_def.io_def.missing_input_messages:
                missing_inputs[exp_id] = command_def.io_def.missing_input_messages
        return missing_inputs

    @staticmethod
    def get_clashing_commands(command_definitions):
        """Reports commands that will overwrite each other's outputs.

        Only reports commands as clashing if they are of the same command type.

        Returns a List[str, List[CommandDefinition]] of output URIs
        and clashing commands.
        """
        outputs_to_defs = {}
        clashing_commands  = []
        for command_def in command_definitions:
            command_type = command_def.command_config.command_type
            for output_uri in command_def.io_def.output_uris:
                if (output_uri, command_type) not in outputs_to_defs:
                    outputs_to_defs[(output_uri, command_type)] = []
                outputs_to_defs[(output_uri, command_type)].append(command_def)

        for ((output_uri, _), command_defs) in outputs_to_defs.items():
            if len(command_defs) > 1:
                clashing_commands.append((output_uri, command_defs))

        return clashing_commands

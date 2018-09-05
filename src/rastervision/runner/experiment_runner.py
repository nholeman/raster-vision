from abc import (ABC, abstractmethod)
from typing import List

import networkx as nx

from rastervision.utils.file imort file_exists

class ExperimentRunner(ABC):
    # TODO: Break this into managable chunks
    def run(self, experiments: List[ExperimentConfig], commands_to_run=rv.ALL_COMMANDS):
        # List of tuples (experiment id, command_type, CommandIODefinition)
        command_definitions = []

        for experiment in experiments:
            e = experiment
            command_definitions = {}
            for command_type in rv.ALL_COMMANDS:
                (e, io_def) = e.preprocess_command(command_type, e)
                command_config = e.make_command_config(command_type)
                command_definitions.append((command_config, io_def))
                if command_type in commands_to_run:
                    for msg in io_def.missing_input_messages:
                        missing_inputs.append("(In experiment {}): {}".format(
                            experiment.id, msg))

        # Filter  out commands we aren't running.
        command_definitions = list(
            filter(lambda c: c[0].command_type in commands_to_run,
                   command_definitions))

        # Check if there are any unsatisfied inputs.
        missing_inputs = {}
        for exp_id, _, io_def in command_definitions:
            if io_def.missing_input_messages:
                missing_inputs[exp_id] = io_def.missing_input_messages
        if missing_inputs:
            # TODO: Replace with logging?
            s = ""
            for exp_id in missing_inputs:
                s += "In {}:\n\t{}\n".format(
                    exp_id,
                    '\t{}\n'.join(missing_inputs[exp_id]))

            raise rv.ConfigurationError("There were missing input URIs "
                                        "that are required, but were not "
                                        "able to be derived: \n{}".format(s))

        # Remove duplicate commands, defining equality for a command by
        # the tuple (command_type, input_uris, output_uris)
        unique_commands = []
        seen_commands = set([])
        for exp_id, command_config, io_def in command_definitions:
            k = (command_config.command_type, io_def.input_uris, io_def.output_uris)
            if not k in s:
                s.add(k)
                unique_commands.append((exp_id, command_config, io_def))

        # Ensure that for each type of command, there are none that clobber
        # each other's output.
        outputs_to_defs = {}
        clashing_msgs  = []
        for exp_id, command_config, io_def:
            for output_uri in io_def.output_uris:
                if output_uri in output_to_defs:
                    if output_to_defs[output_uri][0] == command_config.command_type:
                        command_type = output_to_defs[output_uri][0]
                        other_exp_id = output_to_defs[output_uri][1]
                        clashing_msgs.append("The {} command in both {} and {} experiments "
                                             "output {}, but are not equal.".format(
                                                 command_type, exp_id, other_exp_id, output_uri))

        if clashing_msgs:
            # TODO: Replace with logging?
            s = "\t\n".join(clashing_msgs)

            raise rv.ConfigurationError("ERROR: Command outputs will"
                                        "override each other: \n{}\n".format(s))

        # Create a set of edges, from input_uri to command_config and
        # from command_config to output_uri. Nodes for commands are their
        # index into unique_commands.

        uri_dag = nx.DiGraph()

        for idx, (exp_id, command_config, io_def) in unique_commands:
            for input_uri in io_def.input_uris:
                uri_dag.add_edge(input_uri, idx)

            for output_uri in io_def.output_uris:
                uri_dag.add_edge(idx,  output_uri)

        # Find all source input_uris, and ensure they exist.

        unsolved_sources = [uri
                            for uri in uri_dag.nodes
                            if (type(uri) == str and
                                len(uri_dag.in_edges(uri)) == 0)]

        missing_files = [uri
                         for uri in unsolved_sources
                         if not file_exists(uri)]

        if any(missing_files):
            raise rv.ConfigError("Files do not exist and are not supplied by commands:\n"
                                 "\t{}\n".format(',\b\t'.join(missing_files)))

        # If we are not rerunning, remove commands that have existing outputs.
        # Do this only for ANALYZE and CHIP, as training can continue from
        # checkpoints and affect all downstream processes.
        commands_to_not_rerun = [rv.ANALYZE, rv.CHIP]
        for idx in [idx
                    for idx in uri_dag.nodes
                    if (type(idx) == int and
                        unique_commands[idx][1].command_type in commands_not_to_rerun)]:
            for output_uri in [output_uri
                               for output_uri in dag.out_edges(idx)
                               if file_exists(output_uri)]:
                uri_dag.remove_edge(idx, output_uri)
            if len(dag.out_edges(idx)) == 0:
                uri_dag.remove_node(idx)

        # Collapse the graph to create edges from command to command.
        command_dag = nx.DiGraph()
        for idx in [idx
                    for idx in uri_dag.nodes
                    if (type(idx) == int)]:
            command_dag.add_node(idx)
            for upstream_idx in [upstream_idx
                                 for input_uri in uri_dag.in_edges(idx)
                                 for upstream_idx in uri_dag.in_edges(input_uri)]:
                command_dag.add_edge(upstream_dx, idx)

        # Feed this digraph of commands to the child runner.
        command_list = [command_config
                              for (_, command_config, _) in unique_commands]

        _run_experiment(command_list, command_dag)

    @abstractmethod
    def _run_experiment(self, command_list, command_dag):
        pass

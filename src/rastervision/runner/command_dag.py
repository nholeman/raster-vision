import networkx as nx

class CommandDAG:
    """ A directed acyclic graph of command definitions.
    """
    def __init__(self, command_definitions):
        """Generates a CommandDAG from a list of CommandDefinitions

        This logic checks if there are any non-exsiting URIs that are
        not produced as outputs by some command in the set. If so,
        it raises a ConfigError stating the missing files.
        """
        # Create a set of edges, from input_uri to command_config and
        # from command_config to output_uri. Nodes for commands are their
        # index into unique_commands.

        uri_dag = nx.DiGraph()

        for idx, command_def in enumerate(command_definitions):
            for input_uri in command_def.io_def.input_uris:
                uri_dag.add_edge(input_uri, idx)

            for output_uri in command_def.io_def.output_uris:
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
        # TODO: Solidify this logic.
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
        command_id_dag = nx.DiGraph()
        for idx in [idx
                    for idx in uri_dag.nodes
                    if (type(idx) == int)]:
            command_dag.add_node(idx)
            for upstream_idx in [upstream_idx
                                 for input_uri in uri_dag.in_edges(idx)
                                 for upstream_idx in uri_dag.in_edges(input_uri)]:
                command_dag.add_edge(upstream_dx, idx)

        # Feed this digraph of commands to the child runner.

        self.command_definitions = command_definitions
        self.command_id_dag

    def get_sorted_commands(self):
        """Return a topologically sorted list of commands configurations.

        Returns a list of command configurations that are sorted such that every
        command that depends on some other parent command appears later
        than that parent command.
        """
        return [self.command_definitions[idx].command_config
                for idx in nx.topological_sort(self.command_id_dag)]

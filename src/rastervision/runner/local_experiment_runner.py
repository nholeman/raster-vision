from experiment_runner import *

from tempfile import TemporaryDirectory

class LocalExperimentRunner(ExperimentRunner):
    def _run_experiment(self, commands_list, command_dag):
        """Runs all commands on this machine."""

        with TemporaryDirectory as tmp_dir:
            for idx in nx.topological_sort(command_dag):
                command = command_list[idx].create_command(tmp_dir)
                command.run()

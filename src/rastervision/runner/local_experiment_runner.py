from tempfile import TemporaryDirectory

from rastervision.runner import ExperimentRunner

class LocalExperimentRunner(ExperimentRunner):
    def _run_experiment(self, command_dag):
        """Runs all commands on this machine."""

        with TemporaryDirectory() as tmp_dir:
            for command_config in command_dag.get_sorted_commands():
                command = command_config.create_command(tmp_dir)
                command.run()

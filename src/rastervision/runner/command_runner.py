import tempfile

class CommandRunner:
    @classmethod
    def run(command_name, command_config_json):
        command = get_command(command_name, command_config_json)
        with tempfile.TemporaryDirectory() as tmp_dir:
            command.run(tmp_dir)

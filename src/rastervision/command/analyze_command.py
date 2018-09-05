from rastervision.command import Command

class AnalyzeCommand(Command):
    def __init__(self, scenes, analyzers):
        self.scenes = scenes
        self.analzers = analyzers

    def run(self):
        for analyzer in self.analyzers:
            analyzer.process(self.scenes)

from rastervision.analyzer import Analyzer

class StatsAnalyzer(Analyzer):
    """Computes RasterStats against the entire scene set.
    """

    def __init__(self, stats_uri):
        self.stats_uri = stats_uri

    def process(self, scenes):
        stats = RasterStats()
        stats.compute(list[map(lambda s: s.raster_source, scenes)])
        stats.save(self.stats_uri)

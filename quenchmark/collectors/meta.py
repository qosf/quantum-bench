from quenchmark.plugins import Collector

class MetaCollector(Collector):

    def run(self):

        self.info("I was here")

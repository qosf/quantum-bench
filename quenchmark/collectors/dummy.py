from quenchmark.plugins import Collector


class DummyCollector(Collector):

    def run(self):
        self.info("Dummy collector running")

from quenchmark.plugins import Collector


class DummyCollector(Collector):

    def run(self, project):
        self.info("Dummy collector running")
        return {'result_dummy': project.name}

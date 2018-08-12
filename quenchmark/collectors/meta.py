from quenchmark.plugins import Collector

class MetaCollector(Collector):

    def run(self, project):

        self.info(f"I was here for project: {project.name}")

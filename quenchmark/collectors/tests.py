from quenchmark.plugins import Collector
from quenchmark.utils import run


class TestCollector(Collector):

    def run(self, project):
        if not project.dockerfile:
            self.info("Dockerfile not present")
            return {}

        run([
          'docker', 'build',
          '-t', f'qosstest_{project.identifier]',
          '.'
        ])
        run([
          'docker',
          'run',
          f'qosstest_{project.identifier]',
        ])

        return {'result_dummy': project.name}

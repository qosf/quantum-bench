from quenchmark.plugins import Collector
from quenchmark.utils import run


class TestCollector(Collector):

    def run(self, project):
        if not project.dockerfile:
            self.info("Dockerfile not present")
            return {}

        stdout, stderr, returncode = run([
          'docker', 'build',
          '-t', f'qosstest_{project.identifier}',
          '-f', project.dockerfile,
          '.'
        ])
        self.info(stdout)
        self.info(stderr)

        stdout, stderr, returncode = run([
          'docker',
          'run',
          '--network=host',
          f'qosstest_{project.identifier}',
        ])
        self.info(stdout)
        self.info(stderr)

        return {'result_dummy': project.name}

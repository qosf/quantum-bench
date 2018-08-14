import os
from xml.etree import ElementTree

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

        # Create coverage storage
        os.makedirs('/tmp/quenchmark/reports/', exist_ok=True)

        stdout, stderr, returncode = run([
          'docker',
          'run',
          '--network=host',
          '-v', '/tmp/quenchmark/reports/:/reports/:rw',
          '--security-opt', 'label=type:container_runtime_t',
          f'qosstest_{project.identifier}',
        ])
        self.info(stdout)
        self.info(stderr)

        tree = ElementTree.parse('/tmp/quenchmark/reports/coverage.xml')
        root = tree.getroot()
        self.info(f"{root.attrib}")

        return {
            'coverage_total_lines': root.attrib['lines-valid'],
            'coverage_covered_lines': root.attrib['lines-covered'],
            'coverage_fraction': root.attrib['line-rate']
        }

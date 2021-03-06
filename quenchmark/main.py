import importlib
import pprint
from dataclasses import dataclass

import yaml

import quenchmark.collectors as collectors
from quenchmark.logger import LoggerMixin
from quenchmark.plugins import Collector


@dataclass
class Project:
    name: str
    identifier: str
    repo_url: str
    dockerfile: str = None


class EntryPoint(LoggerMixin):
    """
    The main class that governs the run of the data collection process.
    """

    def import_plugins(self):
        for module in collectors.__all__:
            try:
                module_id = f"{collectors.__name__}.{module}"
                importlib.import_module(module_id)
                self.debug(f"{module_id} loaded successfully.")
            except Exception as exc:
                self.important(f"The module {module} could not be loaded: {exc}")

    def load_configuration(self):
        """
        Loads configuration from the config file and determines the list of
        projects.
        """

        config = yaml.load(open('config.yaml', 'r'))
        self.projects = [
            Project(identifier=identifier, **spec)
            for identifier, spec in config['projects'].items()
        ]

    def collect_data(self):
        """
        Collect data for every project using all available (applicable)
        collectors.
        """

        data = {}

        for project in self.projects:
            project_data = {}

            for plugin_cls in Collector.plugin_classes:
                plugin = plugin_cls()
                new_data = plugin.run(project) or {}
                if set(data.keys()) & set(new_data.keys()):
                    raise Exception("Duplicate key")

                project_data.update(new_data)

            data[project.identifier] = project_data

        return data

    def main(self):
        self.import_plugins()
        self.load_configuration()
        pprint.pprint(self.collect_data())


def main():
    ep = EntryPoint()
    ep.main()

if __name__ == '__main__':
    main()

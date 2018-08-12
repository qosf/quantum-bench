import importlib
from quenchmark.logger import LoggerMixin

import yaml

import quenchmark.collectors as collectors
from quenchmark.plugins import Collector


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
        self.projects = [Project.parse(spec) for spec in config['projects']]

    def collect_data(self):
        for plugin_cls in Collector.plugin_classes:
            plugin = plugin_cls()
            plugin.run()

    def main(self):
        self.import_plugins()
        self.load_configuration()
        self.collect_data()


def main():
    ep = EntryPoint()
    ep.main()

if __name__ == '__main__':
    main()

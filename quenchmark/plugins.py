from quenchmark.logger import LoggerMixin
from quenchmark.utils import classproperty


class NoSuchPlugin(Exception):
    """
    Raised when a plugin could not be found.
    """
    pass


class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        super(PluginMount, cls).__init__(name, bases, attrs)

        if not hasattr(cls, 'plugin_classes'):
            cls.plugin_classes = []
        else:
            cls.plugin_classes.append(cls)


class Collector(LoggerMixin, metaclass=PluginMount):
    """
    Serves as a base class for all collector classes.
    """

    @classproperty
    def plugins(cls):
        """
        Returns a dictionary of Protocol plugins discovered.
        """

        return {
            plugin_class.__name__: plugin_class
            for plugin_class in cls.plugin_classes
        }

    @classmethod
    def get(cls, identifier):
        """
        Returns a plugin class corresponding to the given identifier. Raises
        NoSuchPlugin exception if none was found.
        """

        try:
            return cls.plugins[identifier]
        except KeyError:
            raise NoSuchPlugin(f"Plugin '{identifier}' is not available")

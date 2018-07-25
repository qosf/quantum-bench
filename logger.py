import coloredlogs
import logging
import os


class LoggerMixin(object):
    """
    This mixin adds logging capabilities to a class. All clases inheriting
    from this mixin use the 'main' logger unless overriden otherwise.

    LoggerMixin also provides convenient shortcut methods for logging.
    """

    logger = logging.getLogger('main')

    # Define verbosity levels
    verbosity_to_level = {
        -2: logging.ERROR,
        -1: logging.WARNING,
        0: logging.INFO,
        1: 15,
        2: logging.DEBUG
    }

    # Interface to be leveraged by the class
    @classmethod
    def debug(cls, message, *args):
        cls.logger.debug(message, *args)

    @classmethod
    def verbose(cls, message, *args):
        cls.logger.log(15, message, *args)

    @classmethod
    def info(cls, message, *args):
        cls.logger.info(message, *args)

    @classmethod
    def important(cls, message, *args):
        cls.logger.warning(message, *args)

    @classmethod
    def error(cls, message, *args):
        cls.logger.error(message, *args)

    @classmethod
    def critical(cls, message, *args):
        cls.logger.critical(message, *args)

    # Logging setup related methods
    @classmethod
    def setup_logging(cls):
        """
        Perform the default logging setup.
        """

        # Add custom logging level 'VERBOSE'
        logging.addLevelName(15, "VERBOSE")

        # Setup custom files
        level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
        field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()

        level_styles['debug'] = {'color': 'blue', 'faint': True}
        level_styles['verbose'] = {'color': 'green'}
        level_styles['info'] = {'color': 'yellow'}
        level_styles['warning'] = {'color': 'magenta', 'underline': True}
        level_styles['error'] = {'color': 'red', 'inverse': True}

        field_styles['asctime']['faint'] = True

        coloredlogs.install(
            level=logging.INFO,
            fmt='%(asctime)s: %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
            level_styles=level_styles,
            field_styles=field_styles
        )

    @classmethod
    def set_loglevel(cls, level):
        """
        Set output logging level to given level.
        """

        # Level must fall between <-2, 2>
        if not isinstance(level, int):
            cls.important("Verbosity level must be integer between "
                          f"-2 and 2, not '{level}'")
            cls.important("Setting default verbosity level INFO")
            level = 0
        elif level < -2 or level > 2:
            level = min(max(-2, level), 2)
            cls.important(f"Truncating verbosity level to {level}")

        level_value = cls.verbosity_to_level[level]

        coloredlogs.set_level(level_value)
        cls.info("Setting output logging level to '{}'"
                 .format(logging.getLevelName(level_value)))


# Setup logging
LoggerMixin.setup_logging()

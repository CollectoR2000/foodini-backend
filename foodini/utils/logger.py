import logging
from logging import Formatter, LogRecord

from click import style


def colored_string(string: str, color: str = "cyan", bold: bool = True) -> str:
    return style(str(string), fg=color, bold=bold)


class ColoredFormatter(Formatter):
    levels = {
        logging.DEBUG: lambda levelname: style(str(levelname), fg="cyan"),
        logging.INFO: lambda levelname: style(str(levelname), fg="green"),
        logging.WARNING: lambda levelname: style(str(levelname), fg="yellow"),
        logging.ERROR: lambda levelname: style(str(levelname), fg="red"),
        logging.CRITICAL: lambda levelname: style(str(levelname), fg="bright_red"),
    }

    def __init__(self, name: str, color: str, bold: bool) -> None:
        super().__init__(fmt=f"[%(asctime)s][%(threadName)s][{style(str(name), fg=color, bold=bold)}] %(levelname)s %(message)s")

    def colorize_string(self, string: str, level: int) -> str:
        return self.levels.get(level, lambda string: str(string))(string)

    def formatMessage(self, record: LogRecord) -> str:
        levelname = self.colorize_string(record.levelname, record.levelno)
        seperator = " " * (8 - len(record.levelname))
        record.levelname = f"{levelname}:{seperator}"
        if record.levelno in [logging.ERROR, logging.CRITICAL]:
            record.message = self.colorize_string(record.getMessage(), record.levelno)
        return super().formatMessage(record)


class Logger:
    def __init__(self, name: str, color: str, *, bold: bool = False, level: int = None) -> None:
        if level is None:
            level = logging.DEBUG

        logger = logging.getLogger(name)
        if logger.handlers == []:
            handler = logging.StreamHandler()
            formatter = ColoredFormatter(name, color, bold)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Set log level to the appropriate level.
        logger.setLevel(level)
        # Make sure other loggers do not propagate.
        logger.propagate = False

        # Map logging functions for easy access.
        self.logger = logger
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.critical = self.logger.critical
        self.error = self.logger.error

        # Map the log function for Tenacity.
        self.log = logger.log

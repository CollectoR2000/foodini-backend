from core import settings

from .logger import Logger

log = Logger(settings.PROJECT_TITLE, settings.LOGGING_COLOR)

import logging
import sys

from django.conf import settings
from logging import handlers
from loguru import logger

from log.constants import STDOUT_FORMAT


class Logger:
    def __init__(self,
                 filename,
                 when='D',
                 back_count=3,
                 fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger('lfb')
        format_str = logging.Formatter(fmt)
        if settings.DEBUG:
            th = handlers.TimedRotatingFileHandler(
                filename=filename,
                when=when,
                backupCount=back_count,
                encoding='unt-8')
            console_handler = logging.StreamHandler()
            self.logger.setLevel(logging.DEBUG)
            th.setFormatter(format_str)
            console_handler.setFormatter(format_str)
            self.logger.addHandler(console_handler)
            self.logger.addHandler(th)
        else:
            self.logger.setLevel(logging.INFO)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)


class LXLogger:

    stdout_handler_id = logger.add(sys.stdout, format=STDOUT_FORMAT, catch=False)

    def __init__(self):
        self.logger = logger.bind()

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)


log = Logger('./log_file/llx_log')
lx_log = LXLogger()

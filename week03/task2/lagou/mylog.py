import logging
import os

import settings
from tools import log_lock


def mkdirs(path):
    dir_path, file = os.path.split(path)
    # file_name, ext = os.path.splitext(file)
    if dir_path:
        try:
            os.makedirs(dir_path)
            return path
        except Exception as _:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            # print(f'提供的文件存储目录存在问题，将修改为当前目录{dir_path}')
    return os.path.join(dir_path, file)


class MyLogging:
    def __init__(self, 
                 log_file=settings.LOG_FILE,
                 mode='a',
                 fmt=settings.LOG_FORMAT,
                 level=settings.LOG_LEVEL,
                 stream=False,
                 ):

        self.log_file = mkdirs(log_file)
        self.mode = mode
        self.fmt = fmt
        self.level = level
        self.stream = stream
        self.logger = self._get_logger()

    def _get_logger(self):
        logger = logging.getLogger(self.log_file)
        logger.setLevel(self.level)
        if self.stream:
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(self.log_file,
                                          mode=self.mode,
                                          encoding='utf-8',
                                          delay=False)
        handler.setLevel(self.level)
        handler.setFormatter(logging.Formatter(self.fmt))
        logger.addHandler(handler)
        return logger

    def debug(self, msg, *args, **kwargs):
        with log_lock:
            self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        with log_lock:
            self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        with log_lock:
            self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        with log_lock:
            self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        with log_lock:
            self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        with log_lock:
            self.logger.critical(msg, *args, **kwargs)


logger = MyLogging()
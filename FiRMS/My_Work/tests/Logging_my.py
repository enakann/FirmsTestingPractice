import logging
import sys

class Log:
    def init_logger_singleton(self):
        global logger

        logger = logging.getLogger(name='mylogger')
        logger.setLevel(logging.WARN)
        formatter = logging.Formatter(
            '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s')
        streamhandler = logging.StreamHandler(sys.stdout)
        streamhandler.setLevel(logging.WARNING)
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)
        filehandler = logging.FileHandler('mypython.log')
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

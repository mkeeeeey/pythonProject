import os
import logging
from datetime import datetime
from logging import handlers

Logger = logging.getLogger()


def setLog():

    LogDir = '.'
    if 'APP_LOG_DIR' in os.environ:
        LogDir = os.environ['APP_LOG_DIR']
    logfile = datetime.now().strftime('./LogFile/run_%Y%m%d_%H%M%S%f.log')

    LogHandler = logging.FileHandler(os.path.join(LogDir, logfile))
    Logger.setLevel(logging.INFO)
    LogFormatter = logging.Formatter('[%(asctime)s] - %(message)s')

    LogHandler.setFormatter(LogFormatter)
    Logger.addHandler(LogHandler)

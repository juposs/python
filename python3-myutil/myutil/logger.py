import logzero
from logzero import logger

from myutil import defaults as myutil_defaults

class setup:
    def __init__(self, logfile_path=None, maxBytes=None, backupCount=None):
        """ Sort out the given variables and if neccessary fill in default variables
            or give all parameters:
            log1 = logger.setup("/path/to/logfile", maxBytes=1000, backupCount=10)

            Logfile will rotate after reaching maxBytes, default is '0', never rotate
            If rotation enabled, it will keep 'backupCount' files, default is 10
        """

        self.logfile_path = logfile_path if logfile_path is not None else myutil_defaults.default_logfile_path
        self.maxBytes = maxBytes if maxBytes is not None else myutil_defaults.default_maxBytes
        self.backupCount = backupCount if backupCount is not None else myutil_defaults.backupCount

        logzero.logfile(self.logfile_path, backupCount=self.backupCount, maxBytes=self.maxBytes, disableStderrLogger=True)
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s');
        #logzero.formatter(formatter)

    def info(self, info):
        logger.info(info)
        return None

    def warning(self, warning):
        logger.warning(warning)
        return None

    def error(self, error):
        logger.error(error)
        return None

    def debug(self, debug):
        logger.debug(debug)
        return None

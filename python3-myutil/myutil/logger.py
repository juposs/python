import logzero
from logzero import logger
import os, json

# Import default vars
from myutil import defaults
defaults = defaults.ldap

home = os.path.expanduser("~")
user_settings_file = os.path.join(home, "myutil_settings.json")

defaults = dict(defaults)

if os.path.exists(user_settings_file):
    with open(user_settings_file) as file:
        user_defaults = json.load(file)["logger"]
    defaults.update(user_defaults)

class setup:
    def __init__(self, logfile_path=None, maxBytes=None, backupCount=None):
        """ Sort out the given variables and if neccessary fill in default variables
            or give all parameters:
            log1 = logger.setup("/path/to/logfile", maxBytes=1000, backupCount=10)

            Logfile will rotate after reaching maxBytes, default is '0', never rotate
            If rotation enabled, it will keep 'backupCount' files, default is 10
        """

        self.logfile_path = logfile_path if logfile_path is not None else defaults["logfile_path"]
        self.maxBytes = maxBytes if maxBytes is not None else defaults["maxBytes"]
        self.backupCount = backupCount if backupCount is not None else defaults["backupCount"]

        logzero.logfile(self.logfile_path, backupCount=self.backupCount, maxBytes=self.maxBytes, disableStderrLogger=True)
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s');
        #logzero.formatter(formatter)

    def info(self, info):
        logzero.logfile(self.logfile_path)
        logger.info(info)
        return None

    def warning(self, warning):
        logzero.logfile(self.logfile_path)
        logger.warning(warning)
        return None

    def error(self, error):
        logzero.logfile(self.logfile_path)
        logger.error(error)
        return None

    def debug(self, debug):
        logzero.logfile(self.logfile_path)
        logger.debug(debug)
        return None

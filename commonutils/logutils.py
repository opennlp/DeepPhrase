import datetime
import logging
import daiquiri
from constants import modelconstants


def get_logger(name):
    daiquiri.setup(
        level=logging.DEBUG,
        outputs=(
            daiquiri.output.File(modelconstants.LOG_FILE_PATH, level=logging.DEBUG),
            daiquiri.output.TimedRotatingFile(
                modelconstants.LOG_FILE_PATH,
                level=logging.DEBUG,
                interval=datetime.timedelta(weeks=356))
        )
    )
    logger = daiquiri.getLogger(name)
    return logger

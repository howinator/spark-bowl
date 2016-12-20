import os
import logging


class WrongApplicationIdException(Exception):
    pass


if 'SPARKABOWL_DEBUG_MODE' not in os.environ:
    DEVELOPMENT_ENV = True


def set_logger():
    log = logging.getLogger()
    if DEVELOPMENT_ENV:
        myhandler = logging.StreamHandler()  # writes to stderr
        myformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
        myhandler.setFormatter(myformatter)
        log.addHandler(myhandler)
    return log

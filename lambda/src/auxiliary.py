import os
import logging


class WrongApplicationIdException(Exception):
    pass


class NoValidIntent(Exception):
    pass


def merge_two_dicts(x, y):
    merged = x.copy()
    merged.update(y)
    return merged


def set_logger():
    if 'SPARKABOWL_DEBUG_MODE' not in os.environ:
        dev_env = True
    else:
        dev_env = False
    log = logging.getLogger()
    if dev_env:
        myhandler = logging.StreamHandler()  # writes to stderr
        myformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
        myhandler.setFormatter(myformatter)
        log.addHandler(myhandler)
    return log

__author__ = 'leif'

import logging

logger_name = 'ifind'

def create_ifind_logger(filename):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def get_ifind_logger(name):
    n = '%s.%s' %(logger_name,name)
    logger = logging.getLogger(n)
    return logger



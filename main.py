from PyPhone.PyPhone import PyPhone
import config.config as config
import logging
import sys

if __name__ == '__main__':
    # Setting up log
    logging.basicConfig(level=config.LOG_LEVEL)
    logger = logging.getLogger(__name__)
    logger.info('Logger configured')

    phone = PyPhone()
    phone.run()

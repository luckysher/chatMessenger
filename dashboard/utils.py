import logging

APP_NAME = 'CHATMESS'


def getLogger():
    logging.basicConfig(format='[%(name)][%(levelname)][%(message)]', level=logging.DEBUG)
    return logging.getLogger(APP_NAME)
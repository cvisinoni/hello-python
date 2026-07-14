import logging

import hello


log = logging.getLogger('hello')


if __name__ == '__main__':

    try:
        log.info('where we are going we don\'t need roads')
        log.info(hello)
    except Exception as e:
        log.error("%s", e, exc_info=True)

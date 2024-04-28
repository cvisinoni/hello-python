from hello.logger import log
from hello.config import properties


if __name__ == '__main__':

    log.info('start')

    try:
        log.debug('where we are going we don\'t need roads')
        a = properties.a.b.c.d
    except Exception as e:
        log.error(e)

    log.info('end')

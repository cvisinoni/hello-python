from hello.logger import log


if __name__ == '__main__':

    try:
        log.info('where we are going we don\'t need roads')
        a = 1 / 1
    except Exception as e:
        log.error("%s", e, exc_info=True)

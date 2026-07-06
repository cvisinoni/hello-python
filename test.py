from pathlib import Path
from shutil import rmtree
from os import getlogin

from fork import fork


root = Path(__file__).parent


if __name__ == '__main__':
    rmtree(root / 'test-hello-python', ignore_errors=True)
    fork('fin', root / 'test-hello-python/prjfin', getlogin())
    fork('api', root / 'test-hello-python/prjapi', getlogin())
    fork('lib', root / 'test-hello-python/prjlib', getlogin())

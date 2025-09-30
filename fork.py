from pathlib import Path
import sys


def replace(content: bytes, name: str):
    dictionary = {
        b'hello-python': name.lower().encode('utf-8'),
        b'Hello-Python': name.title().encode('utf-8'),
        b'hello': name.lower().split('-')[0].encode('utf-8')
    }
    for key, value in dictionary.items():
        content = content.replace(key, value)
    return content


def fork(dest):
    root = Path(dest)
    if not root.exists():
        name = root.name
        files = list()
        for relative_path in [
            'hello/__init__.py',
            'hello/config.py',
            'hello/logger.py',
            '.gitignore',
            'LICENSE',
            'local.ini',
            'main.py',
            'README.md',
            'requirements.txt'
        ]:
            src = Path(__file__).parent / relative_path
            dst = root / replace(relative_path.encode('utf-8'), name).decode('utf-8')
            files.append((dst, replace(src.read_bytes(), name)))
        for dst, content in files:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(content)
    else:
        raise FileExistsError(f'{dest} already exists')


if __name__ == '__main__':
    newname = sys.argv[1]
    fork(newname)

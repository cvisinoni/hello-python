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
    project_path = Path(dest)
    name = project_path.name
    project_path.mkdir()
    files = [
        'hello/__init__.py',
        'hello/config.py',
        'hello/logger.py',
        '.gitignore',
        'LICENSE',
        'local.ini',
        'main.py',
        'README.md',
        'requirements.txt'
    ]

    for file in files:
        src = Path(file)
        dst = project_path / replace(file.encode('utf-8'), name).decode('utf-8')
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_bytes()
        content = replace(content, name)
        dst.write_bytes(content)


if __name__ == '__main__':
    newname = sys.argv[1]
    fork(newname)

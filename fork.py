from pathlib import Path
from datetime import datetime
from os import walk
from fnmatch import fnmatch


root: Path = Path(__file__).parent

models = {
    'fin': root / 'final',
    'lib': root / 'library',
    'api': root / 'api',
}


def valid_directory(directory: str):
    return not any([
        fnmatch(directory, '__pycache__'),
        fnmatch(directory, 'venv'),
        fnmatch(directory, '.venv'),
        fnmatch(directory, 'logs'),
    ])


def valid_file(filename: str):
    if fnmatch(filename, '*.pyc'):
        return False
    return True


def replace(content: bytes | str, name: str, owner: str):
    encoding = 'utf-8'
    dictionary = {
        b'hello-python': name.lower().encode(encoding),
        b'Hello-Python': name.title().encode(encoding),
        b'hello': name.lower().split('-')[0].encode(encoding),
        b'$YEAR': str(datetime.now().year).encode(encoding),
        b'$OWNER': owner.encode(encoding),
    }
    for key, value in dictionary.items():
        if isinstance(content, bytes):
            content = content.replace(key, value)
        elif isinstance(content, str):
            content = content.replace(key.decode(encoding), value.decode(encoding))
    return content


def fork(model, dst, owner):
    src: Path = models[model]
    dst: Path = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f'Model {model} not found')
    if dst.exists():
        raise FileExistsError(f'{dst} already exists')

    for s in [src, root / 'all']:
        name = dst.name
        for top, dirs, filenames in walk(s):
            dirs[:] = [d for d in dirs if valid_directory(d)]
            for filename in [f for f in filenames if valid_file(f)]:
                src_file = Path(top) / filename
                rel_path = replace(str(src_file.relative_to(s)), name, owner)
                dst_file = dst / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                dst_file.write_bytes(replace(src_file.read_bytes(), name, owner))
    print(f'Project {model} forked to {dst.absolute()}')


if __name__ == '__main__':
    while True:
        src = input(f"Choose project model {str(tuple(models.keys()))}: ").strip()
        if src in models.keys():
            break
        print("Invalid value")
    dst = input("Insert new project path: ").strip()
    owner = input("Insert project owner: ").strip().lower()
    fork(src, dst, owner)

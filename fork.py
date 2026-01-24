from pathlib import Path
from datetime import datetime
from os import walk


models = {
    'fin': Path(__file__).parent / 'final',
    'lib': Path(__file__).parent / 'library',
}


def replace(content: bytes | str, name: str):
    encoding = 'utf-8'
    dictionary = {
        b'hello-python': name.lower().encode(encoding),
        b'Hello-Python': name.title().encode(encoding),
        b'hello': name.lower().split('-')[0].encode(encoding),
        b'$YEAR': str(datetime.now().year).encode(encoding),
    }
    for key, value in dictionary.items():
        if isinstance(content, bytes):
            content = content.replace(key, value)
        elif isinstance(content, str):
            content = content.replace(key.decode(encoding), value.decode(encoding))
    return content


def fork(model, dst):
    src = models[model]
    dst = Path(dst)
    if not src.exists():
        raise FileNotFoundError(f'Model {model} not found')
    if dst.exists():
        raise FileExistsError(f'{dst} already exists')

    name = dst.name
    for top, dirs, filenames in walk(src):
        for filename in filenames:
            src_file = Path(top) / filename
            rel_path = replace(str(src_file.relative_to(src)), name)
            dst_file = dst / rel_path
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            dst_file.write_bytes(replace(src_file.read_bytes(), name))
    print(f'Project forked to {dst.absolute()}')



if __name__ == '__main__':
    while True:
        src = input(f"Choose project model {str(tuple(models.keys()))}: ").strip()
        if src in models.keys():
            break
        print("Invalid value")
    dst = input("Insert new project path: ").strip()
    fork(src, dst)

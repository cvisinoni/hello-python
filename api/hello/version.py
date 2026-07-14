from datetime import datetime
from pathlib import Path
from hashlib import sha256

from .config import project


def get_fingerprint():
    root = Path(__file__).parent
    files = sorted(root.rglob("*.py"), key=lambda f: f.relative_to(root).as_posix())
    combined = sha256()
    for file in files:
        relpath = file.relative_to(root).as_posix()
        content = file.read_bytes()
        content = content.replace(b"\r\n", b"\n")
        content = content.replace(b"\r", b"\n")
        combined.update(sha256(relpath.encode("utf-8") + b"\0" + content).digest())
    return combined.hexdigest()


def get_banner(build, fingerprint):
    data = dict(
        name=project['name'],
        description=project['description'],
        version=project['version'],
        build=build,
        fingerprint=fingerprint
    )
    file = Path('resources/banner.txt')
    if file.is_file():
        return file.read_text(encoding='utf-8').format_map(data)
    return '\n'.join(
        f'{key + ":":<15} {value}'
        for key, value in data.items()
    )


version = project['version']
build = project['build']
fingerprint = get_fingerprint()
banner = get_banner(build, fingerprint)

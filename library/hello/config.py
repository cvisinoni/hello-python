from pathlib import Path
import tomllib


_pyproject_file = 'pyproject.toml'


def load_project():
    defaults = dict(
        name=__package__,
        description=f'{__package__} project',
        version='0.0.0',
        build=0
    )
    if (path := Path(_pyproject_file)).is_file():
        with path.open("rb") as f:
            content = tomllib.load(f)
        data = {
            str(key).lower(): value
            for key, value in content.items()
        }
        defaults.update(data.get('project', dict()))
    return defaults


project = load_project()

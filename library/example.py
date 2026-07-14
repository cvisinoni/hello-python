from hello.config import project
import json


if __name__ == '__main__':
    print(json.dumps(project, indent=4))

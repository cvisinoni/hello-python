import json
from pathlib import Path

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    salt: str
    role: str


def load_users():
    file = Path('users.json')
    with open(file, mode='r', encoding='utf-8') as fp:
        data = json.load(fp)
    return {key: User(**value) for key, value in data.items()}


users = load_users()

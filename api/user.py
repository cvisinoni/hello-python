import getpass
import json
import secrets
import sys
import hashlib
from pathlib import Path


USERS_FILE = Path('users.json')
ROLES = ('reader', 'writer', 'admin')


def load_users(file: Path) -> dict:
    if file.is_file():
        with file.open('r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_users(file: Path, users: dict) -> None:
    with file.open('w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)
        f.write('\n')


if __name__ == '__main__':

    username = sys.argv[1] if len(sys.argv) > 1 else input("Username: ")
    pwd = sys.argv[2] if len(sys.argv) > 2 else getpass.getpass("Password: ")
    role = sys.argv[3] if len(sys.argv) > 3 else input(f"Role {ROLES}: ")

    if role not in ROLES:
        sys.exit(f"Invalid role: {role!r} (choose from {ROLES})")

    salt = secrets.token_bytes(16)
    hashed = hashlib.scrypt(pwd.encode('utf-8'), salt=salt, n=16384, r=8, p=1, dklen=64)

    users = load_users(USERS_FILE)
    users[username] = {
        "username": username,
        "password": hashed.hex(),
        "salt": salt.hex(),
        "role": role,
    }
    save_users(USERS_FILE, users)
    print(f"User '{username}' saved to {USERS_FILE}")

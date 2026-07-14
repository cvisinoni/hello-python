import hashlib
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from hello.config import config
from hello.users import User, users


basic_auth_security = HTTPBasic()

role_permissions = {
    'admin': {'admin', 'writer', 'reader'},
    'writer': {'writer', 'reader'},
    'reader': {'reader'},
}


def get_current_user(request: Request, credentials: HTTPBasicCredentials = Depends(basic_auth_security)) -> User:
    require_https = config.getbool('auth.require_https', False)
    if require_https and request.url.scheme != 'https':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='HTTPS is required to authenticate',
        )
    user = users.get(credentials.username)
    salt = bytes.fromhex(user.salt) if user else bytes(16)
    computed = hashlib.scrypt(credentials.password.encode('utf-8'), salt=salt, n=16384, r=8, p=1, dklen=64)
    if user is not None and secrets.compare_digest(computed, bytes.fromhex(user.password)):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Authenticate': 'Basic'},
    )


def require_role(minimum_role: str):
    def dependency(user: User = Depends(get_current_user)) -> User:
        if minimum_role not in role_permissions.get(user.role, set()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Insufficient privileges to access this resource',
            )
        return user
    return dependency


BasicReader = Annotated[User, Depends(require_role('reader'))]
BasicWriter = Annotated[User, Depends(require_role('writer'))]
BasicAdmin = Annotated[User, Depends(require_role('admin'))]

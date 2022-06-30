import uuid
from datetime import datetime, timedelta
from typing import Any
from typing import Optional

import pydantic
from jose import jwt
from passlib.context import CryptContext

from config import Config

ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """Generats the hash for the user's password"""
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """Vrifies"""
    return password_context.verify(password, hashed_pass)


class AllOptional(pydantic.main.ModelMetaclass):
    """Can be used to update pydantic schema changing all fields to Optional"""
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


def create_access_token(subject: Any, expires_delta: int = None, **extra_data) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRES)

    to_encode = {"jti": str(uuid.uuid4()), "exp": expires_delta, "sub": str(subject), **extra_data}
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Any, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=Config.JWT_REFRESH_TOKEN_EXPIRES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Config.JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

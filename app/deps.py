from datetime import datetime
from typing import Union

from fastapi import HTTPException, status, Header, Depends
from jose import jwt
from pydantic import ValidationError

from database import User, RevokedTokenModel
from schemas import TokenPayload
from utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)


async def token_data(authorization_token: Union[str, None] = Header(default=None)) -> TokenPayload:
    try:
        payload = jwt.decode(
            authorization_token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        token_data = TokenPayload(**payload)

        if RevokedTokenModel.is_jti_blacklisted(token_data.jti):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data


async def get_current_user(token_data: TokenPayload = Depends(token_data)) -> User:
    user = User.find_by_email(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


async def get_current_librarian(user: User = Depends(get_current_user)) -> User:
    if not user.is_librarian:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    return user

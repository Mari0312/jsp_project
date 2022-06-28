from typing import List

from fastapi import APIRouter, Depends, Query

from database import User
from deps import get_current_librarian, get_current_user
from schemas import RetrieveUser, UpdateUser

router = APIRouter(prefix='/users')


@router.get("/", response_model=List[RetrieveUser])
async def list_users(offset: int = Query(0), limit: int = Query(default=100, lte=100)):
    users = User.list(offset, limit)
    return [RetrieveUser.from_orm(a) for a in users]


@router.get("/{user_id}", response_model=RetrieveUser)
async def get_user(user_id: int, _: User = Depends(get_current_librarian)) -> RetrieveUser:
    user = User.get(user_id)
    return RetrieveUser.from_orm(user)


@router.get("/me/", response_model=RetrieveUser)
async def get_me(user: User = Depends(get_current_user)) -> RetrieveUser:
    return RetrieveUser.from_orm(user)


@router.patch("/me", response_model=RetrieveUser)
async def update_user(user_data: UpdateUser, user: User = Depends(get_current_librarian)):
    User.update(user.id, **dict(user_data))
    user = User.get(user.id)
    return RetrieveUser.from_orm(user)

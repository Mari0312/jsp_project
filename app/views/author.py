from datetime import datetime
from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from database import Author
from utils import AllOptional

router = APIRouter(prefix='/authors')


class CreateAuthor(BaseModel):
    name: str
    date_of_birth: datetime
    date_of_death: datetime = None
    biography: str = None


class UpdateAuthor(CreateAuthor, metaclass=AllOptional):
    ...


class RetrieveAuthor(CreateAuthor):
    id: int

    class Config:
        orm_mode = True


@router.get("/", response_model=List[RetrieveAuthor])
async def list_authors(name: str = Query(None), offset: int = Query(0), limit: int = Query(default=100, lte=100)):
    if name:
        authors = Author.find_by_name(name, offset, limit)
    else:
        authors = Author.list(offset, limit)
    return [RetrieveAuthor.from_orm(a) for a in authors]


@router.get("/{author_id}", response_model=RetrieveAuthor)
async def get_author(author_id) -> RetrieveAuthor:
    author = Author.get(author_id)
    return RetrieveAuthor.from_orm(author)


@router.post("/", response_model=RetrieveAuthor)
async def create_author(create_author: CreateAuthor):
    author = Author(**dict(create_author)).save()
    return RetrieveAuthor.from_orm(author)


@router.patch("/{author_id}", response_model=RetrieveAuthor)
async def update_author(author_id: str, update_author: UpdateAuthor) -> RetrieveAuthor:
    Author.update(author_id, **dict(update_author))
    author = Author.get(author_id)
    return RetrieveAuthor.from_orm(author)


@router.delete("/{author_id}")
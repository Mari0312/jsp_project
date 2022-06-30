from typing import List

from fastapi import APIRouter, Query, Depends

from database import Author, User
from deps import get_current_librarian
from schemas import RetrieveAuthor, CreateAuthor, UpdateAuthor, BaseAuthor

router = APIRouter(prefix='/authors')


@router.get("/", response_model=List[BaseAuthor])
async def list_authors(name: str = Query(None), offset: int = Query(0), limit: int = Query(default=100, lte=100)):
    if name:
        authors = Author.find_by_name(name, offset, limit)
    else:
        authors = Author.list(offset, limit)
    return [RetrieveAuthor.from_orm(a) for a in authors]


@router.get("/{author_id}", response_model=RetrieveAuthor)
async def get_author(author_id: int) -> RetrieveAuthor:
    author = Author.get(author_id)
    return RetrieveAuthor.from_orm(author)


@router.post("/", response_model=RetrieveAuthor)
async def create_author(author_data: CreateAuthor, _: User = Depends(get_current_librarian)):
    author = Author(**author_data.dict(exclude_unset=True)).save()
    return RetrieveAuthor.from_orm(author)


@router.patch("/{author_id}", response_model=RetrieveAuthor)
async def update_author(author_id: int, author_data: UpdateAuthor, _: User = Depends(get_current_librarian)):
    Author.update(author_id, **author_data.dict(exclude_unset=True))
    author = Author.get(author_id)
    return RetrieveAuthor.from_orm(author)

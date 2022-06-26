from datetime import datetime, date
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel as BaseModel_, Field
from starlette import status

from utils import AllOptional


class BaseModel(BaseModel_):

    @classmethod
    def from_orm(cls, obj):
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        return super().from_orm(obj)


class CreateAuthor(BaseModel):
    name: str
    date_of_birth: datetime
    date_of_death: datetime = None
    biography: str = None


class BaseAuthor(BaseModel):
    id: int
    name: str
    date_of_birth: datetime
    date_of_death: datetime = None
    biography: str = None


class UpdateAuthor(CreateAuthor, metaclass=AllOptional):
    ...


class RetrieveAuthor(BaseAuthor):
    books: List['RetrieveBook']

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    jti: str = None
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserSignup(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    first_name: str = Field(..., description="first name")
    last_name: str = Field(..., description="last_name")
    birthday: date = Field(..., description="birtday")
    address: str = Field(..., description="address")
    phone_number: str = Field(..., description="phone_number")


class UserOut(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        orm_mode = True


class CreateGenre(BaseModel):
    name: str


class BaseGenre(BaseModel):
    id: int
    name: str


class RetrieveGenre(BaseGenre):
    id: int
    books: List['RetrieveBook']

    class Config:
        orm_mode = True


class RetrieveBookGenre(CreateGenre):
    id: int

    class Config:
        orm_mode = True


class CreatBook(BaseModel):
    name: str
    description: str
    quantity: int

    genres: List[int]
    authors: List[int]


class UpdateBook(CreatBook, metaclass=AllOptional):
    ...


class RetrieveBookAuthor(CreateAuthor):
    id: int

    class Config:
        orm_mode = True


class RetrieveBook(CreatBook):
    id: int
    authors: List[RetrieveBookAuthor]
    genres: List[RetrieveBookGenre]
    reviews: List['RetrieveReview']
    available_quantity: int

    class Config:
        orm_mode = True


class CreateReview(BaseModel):
    title: str
    created_at: datetime
    rate: int
    content: str


class UpdateReview(CreateReview, metaclass=AllOptional):
    ...


class RetrieveReview(CreateReview):
    id: int
    user: UserOut

    class Config:
        orm_mode = True


RetrieveAuthor.update_forward_refs()
RetrieveGenre.update_forward_refs()
RetrieveBook.update_forward_refs()

from datetime import datetime, date
from typing import List

from pydantic import BaseModel, Field

from utils import AllOptional


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

    class Config:
        orm_mode = True


RetrieveAuthor.update_forward_refs()
RetrieveGenre.update_forward_refs()

from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from starlette import status

from database import Book, User, Genre, BookGenre, session, BookAuthor, Review
from deps import get_current_librarian, get_current_user
from schemas import RetrieveBook, UpdateBook, CreatBook, RetrieveGenre, CreateGenre, BaseGenre, RetrieveReview, \
    CreateReview, UpdateReview

router = APIRouter(prefix='/books')


@router.get("/", response_model=List[RetrieveBook])
async def list_books(name: str = Query(None), offset: int = Query(0), limit: int = Query(default=100, lte=100)):
    if name:
        books = Book.find_by_name(name, offset, limit)
    else:
        books = Book.list(offset, limit)
    return [RetrieveBook.from_orm(a) for a in books]


@router.get("/{book_id}", response_model=RetrieveBook)
async def get_book(book_id: int) -> RetrieveBook:
    book = Book.get(book_id)
    return RetrieveBook.from_orm(book)


@router.post("/", response_model=RetrieveBook)
async def create_book(create_book: CreatBook, _: User = Depends(get_current_librarian)):
    data = dict(create_book)
    genres = data.pop('genres')
    authors = data.pop('authors')

    book = Book(**data).save()

    for author in authors:
        session.add(BookAuthor(book_id=book.id, author_id=author))
    for genre in genres:
        session.add(BookGenre(book_id=book.id, genre_id=genre))

    session.commit()
    return RetrieveBook.from_orm(book)


@router.patch("/{book_id}", response_model=RetrieveBook)
async def update_book(book_id: int, update_book: UpdateBook, _: User = Depends(get_current_librarian)) -> RetrieveBook:
    data = update_book.dict(exclude_unset=True)
    genres = data.pop('genres')
    authors = data.pop('authors')
    Book.update(book_id, **data)
    book = Book.get(book_id)
    book.genres = []
    book.authors = []
    session.commit()
    for author in authors:
        session.add(BookAuthor(book_id=book.id, author_id=author))
    for genre in genres:
        session.add(BookGenre(book_id=book.id, genre_id=genre))

    session.commit()

    return RetrieveBook.from_orm(book)


@router.delete("/{book_id}")
async def delete_book(book_id: int, _: User = Depends(get_current_librarian)):
    count = Book.delete(book_id)
    if count:
        return {"message": "Deleted"}
    return ({"message": "Not found"}), 404


@router.post("/genres/", response_model=RetrieveGenre)
async def create_genre(create_genre: CreateGenre, _: User = Depends(get_current_librarian)):
    genre = Genre(**dict(create_genre)).save()
    return RetrieveGenre.from_orm(genre)


@router.get("/genres/", response_model=List[BaseGenre])
async def list_genres():
    genres = Genre.list_all()
    return [RetrieveGenre.from_orm(a) for a in genres]


@router.get("/genres/{genre_id}", response_model=RetrieveGenre)
async def get_genre(genre_id: int) -> RetrieveGenre:
    genre = Genre.get(genre_id)
    return RetrieveGenre.from_orm(genre)


@router.delete("/genres/{genre_id}")
async def delete_genre(genre_id: int, _: User = Depends(get_current_librarian)):
    count = Genre.delete(genre_id)
    if count:
        return {"message": "Deleted"}
    return {"message": "Not found"}, 404


@router.post("/{book_id}/reviews/", response_model=RetrieveReview)
async def create_review(book_id: int, create_review: CreateReview, user: User = Depends(get_current_user)):
    review = Review(**dict(create_review), book_id=book_id, user_id=user.id).save()
    return RetrieveReview.from_orm(review)


@router.patch("/{book_id}/reviews/{review_id}", response_model=RetrieveReview)
async def update_review(review_id: int, review_data: UpdateReview, user: User = Depends(get_current_user)):
    review = Review.get(review_id)
    if review.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User does not have permissions',
        )
    Review.update(review_id, **review_data.dict(exclude_unset=True))
    review = Review.get(review_id)
    return RetrieveReview.from_orm(review)


@router.delete("/{book_id}/reviews/{review_id}")
async def delete_review_by_id(review_id: int, user: User = Depends(get_current_user)):
    review = Review.get(review_id)
    if review.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User does not have permissions',
        )

    count = Review.delete(review_id)
    if count:
        return {"message": "Deleted"}
    return ({"message": "Not found"}), 404

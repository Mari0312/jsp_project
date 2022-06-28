from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends

from database import Rental, User, RentalBook, session
from deps import get_current_librarian
from schemas import CreateRental, UpdateRental, RetrieveRental

router = APIRouter(prefix='/rentals')


@router.post("/", response_model=RetrieveRental)
async def create_rental(create_rental: CreateRental, user: User = Depends(get_current_librarian)):
    data = dict(create_rental)
    books = data.pop('books')

    rental = Rental(**data, user_id=user.id).save()

    for book in books:
        session.add(RentalBook(rental_id=rental.id, book_id=book))
    session.commit()
    return RetrieveRental.from_orm(rental)


@router.patch("/{rental_id}", response_model=RetrieveRental)
async def update_rental(rental_id: int, update_rental: UpdateRental, _: User = Depends(get_current_librarian)):
    data = dict(update_rental)
    books = data.pop('books')

    Rental.update(rental_id, **data)
    rental = Rental.get(rental_id)
    rental.books = []
    session.commit()
    for book in books:
        session.add(RentalBook(rental_id=rental.id, book_id=book))
    session.commit()
    return RetrieveRental.from_orm(rental)


@router.get("/{rental_id}", response_model=RetrieveRental)
async def get_rental(rental_id: int) -> RetrieveRental:
    rental = Rental.get(rental_id)
    return RetrieveRental.from_orm(rental)


@router.get("/", response_model=List[RetrieveRental])
async def list_rentals():
    rental = Rental.list_all()
    return [RetrieveRental.from_orm(a) for a in rental]


@router.post("/{rental_id}/close")
async def close_rental(rental_id: int, _: User = Depends(get_current_librarian)):
    Rental.update(rental_id, return_date=datetime.utcnow())
    rental = Rental.get(rental_id)
    return RetrieveRental.from_orm(rental)


@router.delete("/{rental_id}")
async def delete(rental_id: int, _: User = Depends(get_current_librarian)):
    count = Rental.delete(rental_id)
    if count:
        return {"message": "Deleted"}
    return ({"message": "Not found"}), 404

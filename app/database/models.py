import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean, and_, Date
from sqlalchemy.orm import relationship

from database import session, Base
from utils import get_hashed_password


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=False)
    address = Column(String(140), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(30), nullable=False)
    hashed_password = Column(String(300), nullable=False)
    is_librarian = Column(Boolean(), default=False)
    rentals = relationship("Rental", backref='user')
    reviews = relationship("Review", backref='user')

    def __init__(self, *args, password, **kwargs):
        super().__init__(hashed_password=get_hashed_password(password), *args, **kwargs)

    @classmethod
    def find_by_first_name(cls, first_name, offset, limit):
        return session.query(cls).filter_by(first_name=first_name) \
            .order_by(cls.id).offset(offset).limit(limit).all()

    @classmethod
    def find_by_last_name(cls, last_name) -> 'User':
        return session.query(cls).filter_by(last_name=last_name).first()

    @classmethod
    def find_by_email(cls, email):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return session.query(cls).filter_by(phone_number=phone_number).first()

    @property
    def additional_claims(self):
        return {"is_librarian": self.is_librarian}


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    books = relationship("Book", secondary='rental_books', back_populates='rentals')

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class RentalBook(Base):
    __tablename__ = "rental_books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)

    rental_id = Column(Integer, ForeignKey('rentals.id', ondelete="CASCADE"), primary_key=True)
    rental = relationship('Rental', primaryjoin='RentalBook.rental_id==Rental.id')


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    authors = relationship("Author", secondary='book_authors', back_populates='books')
    rentals = relationship("Rental", secondary='rental_books', back_populates='books')
    genres = relationship("Genre", secondary='book_genres', back_populates='books')
    reviews = relationship("Review", backref="book")

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()

    @property
    def available_quantity(self):
        return self.quantity - session.query(RentalBook).filter(and_(RentalBook.book_id == self.id,
                                                                     RentalBook.rental.has(return_date=None))).count()


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    books = relationship("Book", secondary='book_genres', back_populates='genres')

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class BookGenre(Base):
    __tablename__ = "book_genres"
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    date_of_death = Column(Date, nullable=True)
    biography = Column(Text, nullable=True)
    books = relationship("Book", secondary='book_authors', back_populates='authors')

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class BookAuthor(Base):
    __tablename__ = 'book_authors'
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete="CASCADE"), primary_key=True)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    rate = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class RevokedTokenModel(Base):
    __tablename__ = 'revoked_tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)

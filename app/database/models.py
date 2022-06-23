import datetime

from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from database.database import session, Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
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

    def __init__(self, *args, password, birthday, **kwargs):
        date_birthday = datetime.date.fromisoformat(birthday)
        super().__init__(hashed_password=self.generate_hash(password), birthday=date_birthday, *args, **kwargs)

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

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @property
    def additional_claims(self):
        return {"is_librarian": self.is_librarian}


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    books = relationship("Book", secondary='rental_books')

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class RentalBook(Base):
    __tablename__ = "rental_books"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'), primary_key=True)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    authors = relationship("Author", secondary='book_authors')
    rentals = relationship("Rental", secondary='rental_books')
    genres = relationship("Genre", secondary='book_genres')
    reviews = relationship("Review", backref="book")

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    books = relationship("Book", secondary='book_genres')

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class BookGenre(Base):
    __tablename__ = "book_genres"
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    date_of_death = Column(DateTime, nullable=False)
    biography = Column(Text, nullable=True)
    books = relationship("Book", secondary='book_authors')

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class BookAuthor(Base):
    __tablename__ = 'book_authors'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), primary_key=True)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False)
    rate = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    @classmethod
    def find_by_name(cls, name, offset, limit):
        return session.query(cls).filter_by(name=name) \
            .order_by(cls.id).offset(offset).limit(limit).all()


class RevokedTokenModel(Base):
    __tablename__ = 'revoked_tokens'
    id = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
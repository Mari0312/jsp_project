from fastapi import FastAPI
from views.author import router as author_router
from views.authorization import router as auth_router
from views.books import router as book_router
from views.rental import router as rental_router
from views.users import router as user_router

app = FastAPI()

app.include_router(author_router)
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(rental_router)
app.include_router(user_router)

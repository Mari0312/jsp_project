from fastapi import FastAPI
from views.author import router as author_router
from views.authorization import router as auth_router
from views.books import router as book_router

app = FastAPI()

app.include_router(author_router)
app.include_router(auth_router)
app.include_router(book_router)

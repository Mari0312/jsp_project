from fastapi import FastAPI
from views.author import router

app = FastAPI()

app.include_router(router)

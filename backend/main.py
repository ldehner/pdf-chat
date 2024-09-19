from fastapi import FastAPI
from controllers import users, documents, chats

app = FastAPI()

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(chats.router)
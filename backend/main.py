from fastapi import FastAPI
from controllers import users, documents, chats
from database.init_database import check_and_init_db

check_and_init_db()

app = FastAPI(debug=True)

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(chats.router)
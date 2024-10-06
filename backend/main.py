from fastapi import FastAPI
from controllers import users, documents, chats
from database.init_database import check_and_init_db
from services.response import preload_model
from fastapi.middleware.cors import CORSMiddleware

check_and_init_db()

preload_model()

app = FastAPI(debug=True)

# Allow CORS from your Angular frontend or any specific origin
origins = [
    "http://localhost:4200",
    # You can add other origins if needed
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(users.router)
app.include_router(documents.router)
app.include_router(chats.router)
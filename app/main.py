from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.document import router as document_router
from app.routers.document_reader import router as reader_router
from app.routers.chatbot import router as chatbot_router



from app.routers import auth
from app.routers import admin

app = FastAPI(
    title="Policy Assistant AI App",
    version="1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(document_router)
app.include_router(reader_router)

app.include_router(chatbot_router)


@app.get("/")
def home():
    return {"message": "Welcome to Policy Assistant AI App!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Customer Support Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Customer Support Bot API is running"}

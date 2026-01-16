from fastapi import FastAPI
from app.core import firebase
from app.api import auth
# uvicorn app:app --reload

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def health():
    return {"status": "ok"}

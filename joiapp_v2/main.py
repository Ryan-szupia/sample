from fastapi import FastAPI
from joiapp_v2.core import firebase
from joiapp_v2.api import auth
# uvicorn app:app --reload

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
def health():
    return {"status": "ok"}

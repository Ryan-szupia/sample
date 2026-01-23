from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from api import auth
from api import prompt
from api import user

# uvicorn app:app --reload
# uvicorn main:app --reload

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(prompt.router, prefix="/api/prompt", tags=["Prompt"])
app.include_router(user.router, prefix="/api/user", tags=["User"])

@app.get("/")
def health():
    return {"status": "ok"}

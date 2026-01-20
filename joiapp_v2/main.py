from fastapi import FastAPI
from joiapp_v2.core import firebase
from joiapp_v2.api import auth
from joiapp_v2.api import prompt
from joiapp_v2.api import user
# uvicorn app:app --reload

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(prompt.router, prefix="/api/prompt", tags=["Prompt"])
app.include_router(prompt.router, prefix="/api/user", tags=["User"])

@app.get("/")
def health():
    return {"status": "ok"}

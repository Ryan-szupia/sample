import os
from dotenv import load_dotenv

load_dotenv

JWT_SECRET_KEY = os.getenv("SECRET_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

missing = []
if not JWT_SECRET_KEY:
    missing.append("SECRET_KEY")
if not OPENAI_API_KEY:
    missing.append("OPENAI_API_KEY")
    
if missing:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
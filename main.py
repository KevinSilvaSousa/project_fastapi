from fastapi import FastAPI  
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

# Iniciar ambiente virtual: venv/scripts/activate
# Iniciar o codico: uvicorn main:app --reload

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQsImV4cCI6MTc3NTY3MjUxNX0.vAIviuGv0N8I9zB540XcW4uImUVWJ-Uz5Ehnbt6ovY4 = cau@gmail.com


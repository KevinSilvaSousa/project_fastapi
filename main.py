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
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Iniciar ambiente virtual: venv/scripts/activate
# Iniciar o codico: uvicorn main:app --reload

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQsImV4cCI6MTc3NTY3MjUxNX0.vAIviuGv0N8I9zB540XcW4uImUVWJ-Uz5Ehnbt6ovY4 = cau@gmail.com

#"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjcsImV4cCI6MTc3NTc2NTYwMH0.pAx9aiNjx_4Arn1VCbibwKQZzhN4fGW2pwOa5ulRSZo",
#  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjcsImV4cCI6MTc3NjM2ODYwMH0.KLxTy5J9yQNHBaHwp36LF2s2kRkVBfcpVuYHvE2BEcE", : Os dois da paty@gmail.com



  #"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjgsImV4cCI6MTc3NTg0MzgyOH0.amAxAyDVEzZ69MOyj3A2ZCCeklWjwSUab7lYnQBbiaw",
 # "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjgsImV4cCI6MTc3NjQ0NjgyOH0.8fZCt7VNrJYQ_hlmGloQeh3Z2z28q4U8oYroHQlSD-k",
  #"token_type": "Bearer"
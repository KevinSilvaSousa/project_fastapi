from fastapi import FastAPI  


app = FastAPI()

# Iniciar o codico: uvicorn main:app --reload

from auth_routes import auth_router
from order_routes import order_router
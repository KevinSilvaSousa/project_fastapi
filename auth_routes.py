from fastapi import APIRouter

auth_router = APIRouter (prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """ 
    Essa e a rota de autenticação
        """
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}
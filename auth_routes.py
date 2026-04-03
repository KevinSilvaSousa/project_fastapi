from fastapi import APIRouter, Depends
from models import Usuario
from dependencias import pegar_secao

auth_router = APIRouter (prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """ 
    Essa e a rota de autenticação
        """
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}


@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_secao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        #ja existe
        return {"messagem", "Já existe um usuario com esse email"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"messagem", "usuario cadastrado"}
    

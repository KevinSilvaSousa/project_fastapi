from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_secao
from main import pwd_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter (prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """ 
    Essa e a rota de autenticação
        """
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session = Depends(pegar_secao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        #ja existe
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        senha_criptografada = pwd_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"messagem", f"usuario cadastrado: {usuario_schema.email}"}
    

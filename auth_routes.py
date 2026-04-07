from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_secao
from main import pwd_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter (prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"fjnfodwn{id_usuario}"
    return token


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif pwd_context.verify(senha, usuario.senha):
        return False
    return usuario


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
    


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_secao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")
    else:
        acess_token = criar_token(usuario.id)
        return {
            "acess_token": acess_token,
            "token_type": "Bearer"            
            }
    

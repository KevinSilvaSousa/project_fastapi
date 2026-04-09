from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_secao, verificar_token
from main import pwd_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter (prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token: timedelta):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado



def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not pwd_context.verify(senha, usuario.senha):
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
        acess_token = criar_token(usuario.id, timedelta(minutes=30))
        refresh_token = criar_token(usuario.id, timedelta(days=7))
        return {
            "access_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"            
            }
    

@auth_router.get("/refresh")
async def user_refresh_token(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return {
            "acess_token": acess_token,
            "token_type": "Bearer"            
            } 



@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_secao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado")
    else:
        acess_token = criar_token(usuario.id, timedelta(minutes=30))
        return {
            "access_token": acess_token,
            "token_type": "Bearer"            
            }
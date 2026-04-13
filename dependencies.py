from fastapi import Depends, HTTPException
from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError

def pegar_secao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_secao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
    except JWTError as error:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do Token")
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido")
    return usuario

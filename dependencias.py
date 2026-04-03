from models import db
from sqlalchemy.orm import sessionmaker
def pegar_secao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
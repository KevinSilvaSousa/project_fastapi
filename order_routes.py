from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_secao, verificar_token
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter (prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])

#Programação Assíncrona permite que seu código execute múltiplas tarefas de I/O concorrentemente sem criar threads. 
#É ideal para operações I/O-bound como requisições HTTP, banco de dados e arquivos.

@order_router.get("/")
async def pedidos():
    """ 
    Essa e a rota de pedidos
        """
    return {"mensagem": "você acessou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_secao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem", f"Pedido criado {novo_pedido.usuario}"}


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int)
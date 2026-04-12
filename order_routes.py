from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_secao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItensPedido

order_router = APIRouter (prefix="/order", tags=["order"] ) # Optional: dependencies=[Depends(verificar_token)] :  (esse codigo ele vira global!)

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
    return {"mensagem": f"Pedido criado {novo_pedido.usuario}"}


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_secao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Sem autorização para isso!")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "messagem": f"Pedido numero: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }



@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_secao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Sem autorização para essa operação!")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
    


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_secao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException (status_code=401, detail="Sem autorização para essa operação!")
    item_pedido = ItensPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "pedido": pedido,
        "preco_pedido": pedido.preco
    }
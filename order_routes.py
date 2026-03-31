from fastapi import APIRouter

order_router = APIRouter (prefix="/order", tags=["order"])

#Programação Assíncrona permite que seu código execute múltiplas tarefas de I/O concorrentemente sem criar threads. 
#É ideal para operações I/O-bound como requisições HTTP, banco de dados e arquivos.

@order_router.get("/")
async def pedidos():
    """ 
    Essa e a rota de pedidos
        """
    return {"mensagem": "você acessou a rota de pedidos"}
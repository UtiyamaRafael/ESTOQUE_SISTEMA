from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    codigo: int
    nome: str
    quantidade: int
    categoria_id: int
    qtd_min: int
    preco_custo: float
    preco_venda: float

class ProdutoCreate(ProdutoBase):
    pass  # por enquanto, criar um produto usa os mesmos campos do Base

class ProdutoOut(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
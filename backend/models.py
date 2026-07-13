from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey, DateTime, Boolean

try:
    from .database import Base
except ImportError:
    from database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer)
    nome = Column(String(100))
    quantidade = Column(Integer)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    qtd_min = Column(Integer)
    preco_custo = Column(Numeric(15, 2))
    preco_venda = Column(Numeric(15, 2))

class Movimentacao(Base):
    __tablename__ = "movimentacao"

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    tipo = Column(Enum("entrada", "saida"))
    quantidade = Column(Integer)
    data = Column(DateTime)
    motivo = Column(String(100))


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100))
    senha = Column(String(100))
    is_admin = Column(Boolean)
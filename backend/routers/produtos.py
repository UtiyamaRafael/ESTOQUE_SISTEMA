from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from ..database import SessionLocal
    from ..models import Produto
    from ..schemas import ProdutoCreate, ProdutoOut
except ImportError:
    from database import SessionLocal
    from models import Produto
    from schemas import ProdutoCreate, ProdutoOut

router = APIRouter(prefix="/produtos", tags=["Produtos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
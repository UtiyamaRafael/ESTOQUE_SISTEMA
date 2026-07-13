try:
    from .database import SessionLocal
    from .models import Categoria
except ImportError:
    from database import SessionLocal
    from models import Categoria

db = SessionLocal()
categorias = db.query(Categoria).all()
print(categorias)
db.close()
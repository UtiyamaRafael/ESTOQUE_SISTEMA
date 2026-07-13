from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql+pymysql://root:root@localhost:3306/estoque")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
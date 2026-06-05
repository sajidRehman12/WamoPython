from sqlalchemy.orm import sessionmaker ,DeclarativeBase

from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

# app/database/database.py
DATABASE_URL = "postgresql+psycopg2://fastapi_user:password123@localhost:5432/fastapi_db"
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

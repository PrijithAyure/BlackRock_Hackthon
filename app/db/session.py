from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# This matches the DATABASE_URL we set in your docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://prijith:securepassword@db:5432/savings_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
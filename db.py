from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQL_DATA= "sqlite:///./todo.db"
engine= create_engine(SQL_DATA, connect_args={"check_same_thread":False})
SessionLocal= sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base= declarative_base()

# Database session manage karne ka function (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
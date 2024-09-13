from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:13ewasz2@172.12.0.15:5432/universidade"
SQLALCHEMY_DATABASE_URL = "postgresql://" + os.environ["DB_USER"] + ":" + os.environ["DB_PASS"] + "@" + os.environ["DB_HOST"] +  ":5432/universidade"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
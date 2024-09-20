from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Professor(Base):
    __tablename__ = 'professor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    cpf = Column(Integer, nullable=False)
    endereco = Column(String(45), nullable=False)
    numero=Column(Integer,nullable=False)
    complemento=Column(String(45),nullable=False)
    cidade=Column(String(45),nullable=False)
    estado=Column(String(45),nullable=False)
    
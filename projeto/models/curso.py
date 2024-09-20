from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Curso(Base):
    __tablename__ = 'curso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    idprofessor=Column(Integer,ForeignKey('professor.id'),nullable=False)
    
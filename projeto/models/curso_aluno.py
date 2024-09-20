from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Curso_Aluno(Base):
    __tablename__ = 'curso_aluno'
    id=Column(Integer, primary_key=True, autoincrement=True)
    id_aluno = Column(Integer, ForeignKey('aluno.id'), nullable=False)
    id_curso = Column(Integer,ForeignKey('curso.id'),nullable=False)
    
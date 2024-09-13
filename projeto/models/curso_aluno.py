from sqlalchemy import Integer, Column, ForeignKey
from .database import Base

class Curso_Aluno(Base):
    __tablename__ = 'curso_aluno'
    
    curso_idcurso = Column(Integer, ForeignKey("cursos.id"), primary_key=True)  # Corrigido o nome da ForeignKey
    aluno_idaluno = Column(Integer, ForeignKey("alunos.id"), primary_key=True)  # Corrigido o nome da ForeignKey

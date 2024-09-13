from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Alunos(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    idade = Column(Integer, nullable=False)
    email = Column(String(20), nullable=False)
    curso = Column(String(50), server_default="Engenharia da Computação")
    periodo = Column(Integer, server_default="0")
    cidade = Column(String(40))
    estado = Column(String(2))
    pais = Column(String(40))
    endereco = Column(String(100))
    turma_id = Column(Integer, ForeignKey('turmas.id'))
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
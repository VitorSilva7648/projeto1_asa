from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Curso(Base):
    __tablename__ = 'curso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    periodo = Column(Integer, nullable=False)
    descricao = Column(String(200), nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    
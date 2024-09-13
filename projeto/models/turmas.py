from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey
from .database import Base

class Turmas(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50), nullable=False)
    campus = Column(String(50), nullable=False)
    # added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))

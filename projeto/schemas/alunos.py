from pydantic import BaseModel

class Aluno(BaseModel):
    nome: str
    idade: int
    email: str
    curso: str
    periodo: int
    cidade: str
    estado: str
    pais: str
    turma_id: int

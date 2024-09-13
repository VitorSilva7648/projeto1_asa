from pydantic import BaseModel

class Turma(BaseModel):
    descricao: str
    campus: str

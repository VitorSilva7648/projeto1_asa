from pydantic import BaseModel

class Curso(BaseModel):
    nome: str
    idprofessor: int
from pydantic import BaseModel

class Curso(BaseModel):
    idCurso: int
    nome: str
    professor_idprofessor: int


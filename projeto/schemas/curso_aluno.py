from pydantic import BaseModel

class Curso_Aluno(BaseModel):
    Curso_idCurso: int
    Aluno_idAluno: int

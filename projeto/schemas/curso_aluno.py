from pydantic import BaseModel

class Curso_Aluno(BaseModel):
    id_curso: int
    id_aluno: int
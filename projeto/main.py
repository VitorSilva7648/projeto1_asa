from fastapi import FastAPI
from typing import Optional
from routers.alunos import router as router_alunos
# from routers.turmas import router as router_turmas
from models.database import engine
from models.alunos import Aluno
from models.alunos import Base
from routers.professor import router as router_professor
from routers.curso_aluno import router as router_curso_aluno
from routers.cursos import router as router_curso

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_alunos)
app.include_router(router_professor)
app.include_router(router_curso)
app.include_router(router_curso_aluno)
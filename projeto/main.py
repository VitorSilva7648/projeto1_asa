from fastapi import FastAPI
from typing import Optional
from routers.alunos import router as router_alunos
from routers.turmas import router as router_turmas
from models.database import engine
from models.alunos import Alunos
from models.alunos import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_alunos)
app.include_router(router_turmas)
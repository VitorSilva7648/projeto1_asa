from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas.curso import Curso
from models.database import get_db
from models.curso import Curso as Cursos
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/cursos")
def todos_cursos(db: Session = Depends(get_db)):
    all_cursos = db.query(Cursos).all()
    return all_cursos


@router.post("/cursos")
async def criar_curso(curso: Curso, db: Session = Depends(get_db)):
    novo_curso = Cursos(**curso.model_dump())  # Usar o modelo SQLAlchemy
    try:
        db.add(novo_curso)
        db.commit()
        db.refresh(novo_curso)
        logging.info("Curso criado com sucesso")
        return { "mensagem": "Curso criado com sucesso", "curso": novo_curso}
    except Exception as e:
        logging.error(e)
        return { "mensagem": "Problemas para inserir o curso"}


@router.delete("/cursos/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(Cursos).filter(Cursos.id == id).first()  # .first() precisa ser adicionado
    
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso não existe")
    else:
        db.delete(delete_post)  # Correção para deletar o objeto diretamente
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/cursos/{id}")
def update(id: int, curso: Curso, db: Session = Depends(get_db)):
    updated_post = db.query(Cursos).filter(Cursos.id == id)
    updated_post.first()  # Obter o primeiro resultado
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso: {id} não existe")
    else:
        updated_post.update(curso.model_dump(), synchronize_session=False)  # Atualizar diretamente o objeto
        db.commit()
    return updated_post.first()
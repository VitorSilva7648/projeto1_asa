from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.alunos   import Aluno
from models.database  import get_db
from models.alunos    import Alunos
from sqlalchemy.orm   import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


router = APIRouter()

@router.get("/alunos")
def get(db: Session = Depends(get_db)):
    all_alunos = db.query(Alunos).all()
    logging.info("GET_ALL_ALUNOS")
    alunos = []
    for aluno in all_alunos:
        item = {"id": aluno.id,
                "nome": aluno.nome}
        alunos.append(item)       
    logging.info(alunos)
    return all_alunos


@router.post("/alunos")
async def criar_aluno(aluno: Aluno, db: Session = Depends(get_db)):
    novo_aluno = Alunos(**aluno.model_dump())
    try:
        
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        logging.info("Aluno criado com sucesso")
        return { "mensagem": "Aluno criado com sucesso",
                 "aluno": novo_aluno}
    except Exception as e:
            logging.error(e)
            return { "mensagem": "Problemas para inserir o aluno",
                 "aluno": novo_aluno}
 
@router.delete("/alunos/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Alunos).filter(Alunos.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/alunos/{id}")
def update(id: int, aluno:Aluno, db:Session = Depends(get_db)):
    updated_post = db.query(Alunos).filter(Alunos.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Aluno: {id} does not exist')
    else:
        updated_post.update(aluno.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()
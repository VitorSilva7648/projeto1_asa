from fastapi          import APIRouter, Depends, HTTPException, Response, status
from schemas.turmas   import Turma
from models.database  import get_db
from models.turmas    import Turmas
from sqlalchemy.orm   import Session

router = APIRouter()

@router.get("/turmas")
def get(db: Session = Depends(get_db)):
    all_turmas = db.query(Turmas).all()
    return all_turmas


@router.post("/turmas")
async def criar_turmas(turma: Turma, db: Session = Depends(get_db)):
    nova_turma = Turmas(**turma.model_dump())
    try:
        db.add(nova_turma)
        db.commit()
        db.refresh(nova_turma)
        return { "mensagem": "Aluno criado com sucesso",
                 "nova_turma": nova_turma}
    except Exception as e:
            print(e)
            return { "mensagem": "Problemas para inserir o aluno",
                 "nova_turma": nova_turma}

 
@router.delete("/turmas/{id}")
def delete(id:int ,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Turmas).filter(Turmas.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/turmas/{id}")
def update(id: int, turma:Turma, db:Session = Depends(get_db)):
    updated_post = db.query(Turmas).filter(Turmas.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Aluno: {id} does not exist')
    else:
        updated_post.update(turma.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()
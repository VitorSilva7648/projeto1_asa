from fastapi          import APIRouter, Depends, HTTPException, Response, status
from models.professor    import Professor as Professores
from schemas.professor   import Professor
from models.database  import get_db
from sqlalchemy.orm   import Session

router = APIRouter()

@router.get("/professores")
def todos_professores(db: Session = Depends(get_db)):
    all_professores = db.query(Professores).all()
    professores = []
    for professor in all_professores:
        item =  {
                "id": professor.id,
                "nome": professor.nome,
                "email": professor.email,
                "cpf": professor.cpf,
                "endereco": professor.endereco,
                "numero": professor.numero,
                "complemento": professor.complemento,
                "cidade": professor.cidade,
                "estado": professor.estado
                }
        professores.append(item)       
    return professores

@router.get("/professores/{id}")
async def professor_por_id(id:int,db: Session = Depends(get_db)):
    professor=db.query(Professores).filter(Professores.id==id).first()
    if(professor==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor não existe")
    else:
        return professor
        

@router.post("/professores")
async def criar_professor(professor: Professor, db: Session = Depends(get_db)):
    novo_professor = Professores(**professor.model_dump())
    try:
        db.add(novo_professor)
        db.commit()
        db.refresh(novo_professor)
        return { "mensagem": "Professor criado com sucesso",
                 "professor": novo_professor}
    except Exception as e:
        return { "mensagem": "Problemas para inserir o professor",
                 "professor": novo_professor}
 
@router.delete("/professores/{id}")
def delete(id: int, db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Professores).filter(Professores.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professor não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/professores/{id}")
def update(id: int, professor: Professor, db: Session = Depends(get_db)):
    updated_post = db.query(Professores).filter(Professores.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Professor: {id} não existe')
    else:
        updated_post.update(professor.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()

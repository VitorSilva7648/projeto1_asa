from fastapi          import APIRouter, Depends, HTTPException, Response, status
from models.alunos    import Aluno as Alunos
from schemas.alunos   import Aluno
from models.database  import get_db
from sqlalchemy.orm   import Session

router = APIRouter()

@router.get("/alunos")
def get(db: Session = Depends(get_db)):
    all_alunos = db.query(Alunos).all()
    # alunos = []
    # for aluno in all_alunos:
    #     item =  {
    #             "id": aluno.id,
    #             "nome": aluno.nome,
    #             "email": aluno.email,
    #             "cpf": aluno.cpf,
    #             "endereco": aluno.endereco,
    #             "numero": aluno.numero,
    #             "complemento": aluno.complemento,
    #             "cidade": aluno.cidade,
    #             "estado": aluno.estado
    #             }
    #     alunos.append(item)       
    return all_alunos

@router.get("/alunos/{id}")
async def aluno_por_id(id:int,db: Session = Depends(get_db)):
    aluno=db.query(Alunos).filter(Alunos.id==id).first()
    if(aluno==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno não existe")
    else:
        return aluno
        

@router.post("/alunos")
async def criar_aluno(aluno: Aluno, db: Session = Depends(get_db)):
    novo_aluno = Alunos(**aluno.model_dump())
    try:
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return { "mensagem": "Aluno criado com sucesso",
                 "aluno": novo_aluno}
    except Exception as e:
        return { "mensagem": "Problemas para inserir o aluno",
                 "aluno": novo_aluno}
 
@router.delete("/alunos/{id}")
def delete(id: int, db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT):
    delete_post = db.query(Alunos).filter(Alunos.id == id)
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aluno não existe")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)   


@router.put("/alunos/{id}")
def update(id: int, aluno: Aluno, db: Session = Depends(get_db)):
    updated_post = db.query(Alunos).filter(Alunos.id == id)
    updated_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Aluno: {id} não existe')
    else:
        updated_post.update(aluno.model_dump(), synchronize_session=False)
        db.commit()
    return updated_post.first()

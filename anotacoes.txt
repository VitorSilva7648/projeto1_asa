from fastapi import APIRouter, Depends, HTTPException, status
from schemas.curso_aluno import Curso_Aluno
from models.curso_aluno import Curso_Aluno as Curso_Aluno_Model  # Importando corretamente o modelo SQLAlchemy
from models.database import get_db
from sqlalchemy.orm import Session
from models.curso import Curso
from models.alunos import Aluno
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# Get all relationships between courses and students
@router.get("/curso_aluno")
def get_all_curso_aluno(db: Session = Depends(get_db)):
    all_curso_aluno = db.query(Curso_Aluno_Model).all()
    curso_alunos=[]
    for curso_aluno in all_curso_aluno:
        curso=db.query(Curso).filter(Curso.id==curso_aluno.id_curso).first()
        aluno=db.query(Aluno).filter(Aluno.id==curso_aluno.id_aluno).first()
        curso_alunos.append(curso)
        curso_alunos.append(aluno)
    return curso_alunos

# Get a specific course-student relationship
@router.get("/curso_aluno/{curso_idcurso}/{aluno_idaluno}")
def get_curso_aluno(curso_idcurso: int, aluno_idaluno: int, db: Session = Depends(get_db)):
    curso_aluno = db.query(Curso_Aluno_Model).filter_by(curso_idcurso=curso_idcurso, aluno_idaluno=aluno_idaluno).first()
    
    if not curso_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relação curso-aluno não encontrada")
    
    return curso_aluno

# Create a new course-student relationship
@router.post("/curso_aluno")
async def criar_curso_aluno(curso_aluno: Curso_Aluno, db: Session = Depends(get_db)):
    novo_curso_aluno = Curso_Aluno_Model(**curso_aluno.model_dump())
    
    try:
        db.add(novo_curso_aluno)
        db.commit()
        return {"mensagem": "Curso-Aluno criado com sucesso", "curso_aluno": novo_curso_aluno}
    except Exception as e:
        logging.error(e)
        db.rollback()  # Reverter caso haja um erro
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problemas ao criar curso-aluno")

# Delete a course-student relationship
@router.delete("/curso_aluno/{curso_idcurso}/{aluno_idaluno}")
def delete_curso_aluno(curso_idcurso: int, aluno_idaluno: int, db: Session = Depends(get_db)):
    curso_aluno = db.query(Curso_Aluno_Model).filter_by(curso_idcurso=curso_idcurso, aluno_idaluno=aluno_idaluno).first()
    
    if not curso_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relação curso-aluno não encontrada")
    
    db.delete(curso_aluno)
    db.commit()
    logging.info(f"Curso-Aluno deletado: Curso {curso_idcurso}, Aluno {aluno_idaluno}")
    
    return {"mensagem": "Curso-Aluno deletado com sucesso"}

# Update a course-student relationship
@router.put("/curso_aluno/{curso_idcurso}/{aluno_idaluno}")
def update_curso_aluno(curso_idcurso: int, aluno_idaluno: int, curso_aluno: Curso_Aluno, db: Session = Depends(get_db)):
    curso_aluno_db = db.query(Curso_Aluno_Model).filter_by(curso_idcurso=curso_idcurso, aluno_idaluno=aluno_idaluno).first()
    
    if not curso_aluno_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relação curso-aluno não encontrada")
    
    # Atualiza o relacionamento
    for key, value in curso_aluno.dict().items():
        setattr(curso_aluno_db, key, value)
    
    db.commit()
    logging.info(f"Curso-Aluno atualizado: Curso {curso_idcurso}, Aluno {aluno_idaluno}")
    
    return {"mensagem": "Curso-Aluno atualizado com sucesso", "curso_aluno": curso_aluno_db}

@router.get("/curso_aluno/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(Curso_Aluno).filter(Curso_Aluno.id == id).first()  # .first() precisa ser adicionado
    
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso_Aluno não existe")
    else:
        db.delete(delete_post)  # Correção para deletar o objeto diretamente
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/curso_aluno/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(Curso_Aluno).filter(Curso_Aluno.id == id).first()  # .first() precisa ser adicionado
    
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso_Aluno não existe")
    else:
        db.delete(delete_post)  # Correção para deletar o objeto diretamente
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/curso_aluno/{id}")
def update(id: int, curso: Curso_Aluno, db: Session = Depends(get_db)):
    updated_post = db.query(Curso_Aluno).filter(Curso_Aluno.id == id)
    updated_post.first()  # Obter o primeiro resultado
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso: {id} não existe")
    else:
        updated_post.update(curso.model_dump(), synchronize_session=False)  # Atualizar diretamente o objeto
        db.commit()
    return updated_post.first()

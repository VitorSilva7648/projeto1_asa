from fastapi import APIRouter, Depends, HTTPException, status
from schemas.curso_aluno import Curso_Aluno
from models.curso_aluno import Curso_Aluno as Curso_Aluno_Model  # Importando corretamente o modelo SQLAlchemy
from models.database import get_db
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# Get all relationships between courses and students
@router.get("/curso_aluno")
def get_all_curso_aluno(db: Session = Depends(get_db)):
    all_curso_aluno = db.query(Curso_Aluno_Model).all()
    logging.info("GET_ALL_CURSO_ALUNO")
    
    return all_curso_aluno

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
    novo_curso_aluno = Curso_Aluno_Model(**curso_aluno.dict())
    
    try:
        db.add(novo_curso_aluno)
        db.commit()
        logging.info(f"Curso-Aluno criado: Curso {curso_aluno.curso_idcurso}, Aluno {curso_aluno.aluno_idaluno}")
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

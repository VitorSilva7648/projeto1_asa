from pydantic import BaseModel

class Aluno(BaseModel):
    nome: str
    email: str
    cpf: int
    endereco: str 
    numero: int 
    complemento: str
    cidade: str
    estado: str
    

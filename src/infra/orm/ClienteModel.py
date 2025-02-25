import db
from sqlalchemy import Column, VARCHAR, Integer

class ClienteDB(db.Base):
    __tablename__ = 'tb_cliente'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    cpf = Column(VARCHAR(11), nullable=False, unique=True) 
    telefone = Column(VARCHAR(15), nullable=False)  

import db
from sqlalchemy import Column, VARCHAR, Integer, Float, LargeBinary

class ProdutoDB(db.Base):
    __tablename__ = 'tb_produto'

    id_produto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    descricao = Column(VARCHAR(255), nullable=True)
    valor_unitario = Column(Float, nullable=False)
    foto = Column(LargeBinary, nullable=True)

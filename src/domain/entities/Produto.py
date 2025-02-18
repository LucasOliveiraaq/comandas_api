from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    id_produto: Optional[int] = None
    nome: str
    descricao: Optional[str] = None
    valor_unitario: float  
    foto: Optional[bytes] = None 



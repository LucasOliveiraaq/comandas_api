# Lucas Pinheiro de Oliveira

from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

from app import FuncionarioDAO
from app import ClienteDAO
from app import ProdutoDAO

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa no startup
    print("API has started")
    import db
    await db.criaTabelas()
    yield
    # Executa no shutdown
    print("API is shutting down")

# Cria a aplicação FastAPI com o contexto de vida
app = FastAPI(lifespan=lifespan)

# Mapeamento das rotas/endpoints
app.include_router(FuncionarioDAO.router)
app.include_router(ClienteDAO.router)
app.include_router(ProdutoDAO.router)

# Rota padrão
@app.get("/")
def root():
    return {"detail": "API Pastelaria", "Swagger UI": "http://127.0.0.1:8000/docs", "ReDoc": "http://127.0.0.1:8000/redoc"}

if __name__ == "__main__":
    uvicorn.run('main:app', host=HOST, port=PORT, reload=RELOAD)

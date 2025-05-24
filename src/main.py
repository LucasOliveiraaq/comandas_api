# Lucas Pinheiro de Oliveira

from fastapi import FastAPI
from src.settings import HOST, PORT, RELOAD
from src import security
import uvicorn

import src.security
from src.app import FuncionarioDAO
from src.app import ClienteDAO
from src.app import ProdutoDAO
from src.app import ComandaDAO

from contextlib import asynccontextmanager
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import src.db

# Tenta conectar ao banco com retry
def aguardar_conexao_banco():
    DATABASE_URL = "postgresql+psycopg2://postgres:postgre@db:5432/comandas_db"
    MAX_RETRIES = 10
    WAIT_SECONDS = 3

    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            print(f"⏳ Tentando conectar ao banco (tentativa {tentativa})...")
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            print("✅ Conexão com banco bem-sucedida!")
            break
        except OperationalError as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            if tentativa == MAX_RETRIES:
                print("💥 Não foi possível conectar ao banco. Abortando.")
                raise e
            time.sleep(WAIT_SECONDS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Inicializando API")
    aguardar_conexao_banco()
    await src.db.criaTabelas()
    yield
    print("🛑 Encerrando API")

# Cria a aplicação FastAPI com o contexto de vida
app = FastAPI(lifespan=lifespan)

# Mapeamento das rotas/endpoints
app.include_router(security.router)
app.include_router(FuncionarioDAO.router)
app.include_router(ClienteDAO.router)
app.include_router(ProdutoDAO.router)
app.include_router(ComandaDAO.router)

@app.get("/")
def root():
    return {
        "detail": "API Pastelaria",
        "Swagger UI": "https://127.0.0.1:8000/docs",
        "ReDoc": "https://127.0.0.1:8000/redoc"
    }

if __name__ == "__main__":
    import ssl
    import hypercorn.asyncio
    from hypercorn.config import Config
    import asyncio

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert/cert.pem", keyfile="cert/ecc-key.pem")
    #ssl_context.load_cert_chain(certfile="cert/cert.pem", keyfile="cert/ecc-key.pem")

    config = Config()
    config.bind = ["0.0.0.0:4443"]
    config.quic_bind = ["0.0.0.0:4443"]
    config.certfile = "cert/cert.pem"
    #config.certfile = "cert/cert.pem"
    #config.keyfile = "cert/ecc-key.pem"
    config.keyfile = "cert/ecc-key.pem"
    config.alpn_protocols = ["h2", "h3"]

    asyncio.run(hypercorn.asyncio.serve(app, config))



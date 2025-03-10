from dotenv import load_dotenv, find_dotenv
import os

# Localiza o arquivo .env e carrega as variáveis de ambiente
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

# Configurações da API
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True").lower() == "true"

# Configurações do banco de dados
DB_SGDB = os.getenv("DB_SGDB", "sqlite")
DB_NAME = os.getenv("DB_NAME", "apiDatabase")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")  # Adicionando a porta
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgre")

# Ajusta STR_DATABASE conforme o SGBD escolhido
if DB_SGDB == 'sqlite':  # SQLite
    STR_DATABASE = f"sqlite:///{DB_NAME}.db"
elif DB_SGDB == 'mysql':  # MySQL
    import pymysql
    STR_DATABASE = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
elif DB_SGDB == 'mssql':  # SQL Server
    import pymssql
    STR_DATABASE = f"mssql+pymssql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
elif DB_SGDB == 'postgresql':  # PostgreSQL
    import psycopg2
    STR_DATABASE = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:  # Default SQLite
    STR_DATABASE = f"sqlite:///apiDatabase.db"

print("String de conexão:", STR_DATABASE)

# Configurações Segurança da API
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

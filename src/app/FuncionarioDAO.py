# Lucas Pinheiro de Oliveira

from fastapi import APIRouter, Depends
from typing import Annotated
from src.domain.entities.Funcionario import Funcionario
import src.db
from src.infra.orm.FuncionarioModel import FuncionarioDB
from src.security import get_current_active_user, User
import bcrypt

router = APIRouter(dependencies=[Depends(get_current_active_user)])

@router.get("/funcionario/", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)])
async def get_funcionario(current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        session = src.db.Session()
        dados = session.query(FuncionarioDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario(id: int):
    try:
        session = src.db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"])
async def post_funcionario(corpo: Funcionario):
    try:
        session = src.db.Session()
        senha_hash = bcrypt.hashpw(corpo.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        dados = FuncionarioDB(
            nome=corpo.nome,
            matricula=corpo.matricula,
            cpf=corpo.cpf,
            telefone=corpo.telefone,
            grupo=corpo.grupo,
            senha=senha_hash
        )
        session.add(dados)
        session.commit()
        session.refresh(dados)
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/funcionario/{id}", tags=["Funcionário"])
async def put_funcionario(id: int, corpo: Funcionario):
    try:
        session = src.db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        dados.matricula = corpo.matricula
        dados.grupo = corpo.grupo

        if corpo.senha:
            dados.senha = bcrypt.hashpw(corpo.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/funcionario/{id}", tags=["Funcionário"])
async def delete_funcionario(id: int):
    try:
        session = src.db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/login/", tags=["Funcionário - Login"])
async def login_funcionario(corpo: Funcionario):
    try:
        session = src.db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).one()

        if bcrypt.checkpw(corpo.senha.encode('utf-8'), dados.senha.encode('utf-8')):
            return dados, 200
        else:
            return {"erro": "CPF ou senha inválidos"}, 401

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_funcionario(cpf: str):
    try:
        session = src.db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

#Lucas Pinheiro de Oliveira

from fastapi import APIRouter
from src.domain.entities.Cliente import Cliente

import src.db
from src.infra.orm.ClienteModel import ClienteDB

from typing import Annotated
from fastapi import Depends
from src.security import get_current_active_user, User

router = APIRouter(dependencies=[Depends(get_current_active_user)])
# Criar as rotas/endpoints: GET, POST, PUT, DELETE

@router.get("/cliente/", tags=["Cliente"], dependencies=[Depends(get_current_active_user)],)
async def get_cliente(current_user:Annotated[User, Depends(get_current_active_user)],):
    try:
        session = src.db.Session()
        # busca todos
        dados = session.query(ClienteDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()


@router.get("/cliente/{id}", tags=["Cliente"])
async def get_cliente(id: int):
    try:
        session = src.db.Session()
        # busca um com filtro
        dados = session.query(ClienteDB).filter(
            ClienteDB.id_cliente == id).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()


@router.post("/cliente/", tags=["Cliente"])
async def post_cliente(corpo: Cliente):
    try:
        session = src.db.Session()
        dados = ClienteDB(
            nome=corpo.nome,
            cpf=corpo.cpf,
            telefone=corpo.telefone
        )
        session.add(dados)
        session.commit()
        session.refresh(dados)
        return {"id": dados.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


@router.put("/cliente/{id}", tags=["Cliente"])
async def put_cliente(id: int, corpo: Cliente):
    try:
        session = src.db.Session()
        # busca os dados atuais pelo id
        dados = session.query(ClienteDB).filter(
            ClienteDB.id_cliente == id).one()
        # atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        session.add(dados)
        session.commit()
        return {"id": dados.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


@router.delete("/cliente/{id}", tags=["Cliente"])
async def delete_cliente(id: int):
    try:
        session = src.db.Session()
        # busca os dados atuais pelo id
        dados = session.query(ClienteDB).filter(
            ClienteDB.id_cliente == id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Valida o CPF informado pelo cliente
@router.get("/cliente/cpf/{cpf}", tags=["Cliente - Valida CPF"])
async def cpf_cliente(cpf: str):
    try:
        session = src.db.Session()
        # busca um com filtro, retornando os dados cadastrados
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == cpf).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

from pydantic import BaseModel
from typing import List
from model.ordem import Ordem
from datetime import datetime

from schemas.produto import *


class OrdemSchema(BaseModel):
    """ Define como uma nova ordem a ser inserida deve ser representada
    """
    produtos: List[ProdutoSchema]    


class OrdemViewSchema(BaseModel):
    """ Define como uma ordem será retornado: ordem + produtos.
    """
    id: int = 1
    data_criacao: datetime = "dd/MM/yyyy"
    produtos: List[ProdutoSchema]


class OrdemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_ordem(ordem: Ordem):
    """ Retorna uma representação da ordem seguindo o schema definido em
        OrdemViewSchema.
    """
    return {
        "id": ordem.id,
        "data_criacao": ordem.create_time
    }
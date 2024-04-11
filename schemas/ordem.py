from pydantic import BaseModel
from typing import List
from model.ordem import Ordem
from datetime import datetime

from schemas.produto import *


class OrdemSchema(BaseModel):
    """ Define como uma nova ordem a ser inserida deve ser representada
    """
    produtos: List[ProdutoSchema]    


class OrdemBuscaSchema(BaseModel):
    """ Define como uma ordem será retornado: ordem + produtos.
    """
    id: int = 0


class OrdemViewSchema(BaseModel):
    """ Define como uma ordem será retornado: ordem + produtos.
    """
    id: int = 1
    data_criacao: datetime = "dd/MM/yyyy"
    produtos: List[ProdutoSchema]


class OrdemListViewSchema(BaseModel):
    """ Define como uma ordem será retornado: ordem + produtos.
    """
    ordens: List[OrdemViewSchema]


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


    mascara = "%d/%m/%Y %H:%M:%S"

    return {
        "id": ordem.id,
        "data_criacao": ordem.create_time.strftime(mascara),
        "produtos": [{"nome": p.nome,"quantidade": p.quantidade} for p in ordem.produtos]
    }


def apresenta_ordens(ordens: List[Ordem]):
    """ Retorna uma representação de um conjunto de ordens seguindo o schema definido em
        OrdemListViewSchema.
    """
    
    
    mascara = "%d/%m/%Y %H:%M:%S"
    
    return {
        "ordens": [{"id": o.id,
                    "data_criacao": o.create_time.strftime(mascara),
                    "produtos": [{"nome": p.nome,"quantidade": p.quantidade} for p in o.produtos]} for o in ordens]
    }
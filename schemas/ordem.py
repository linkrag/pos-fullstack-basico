from pydantic import BaseModel
from typing import List
from model.ordem import Ordem
from datetime import datetime

from schemas.produto import *
from schemas.observacao import *


class OrdemSchema(BaseModel):
    """ Define como uma nova ordem a ser inserida deve ser representada
    """
    produtos: List[ProdutoSchema]    


class OrdemBuscaSchema(BaseModel):
    """ Define como uma ordem deverá ser buscada.
    """
    ordem_id: int = 0


class OrdemViewSchema(BaseModel):
    """ Define como uma ordem deverá ser representada.
    """
    id: int = 1
    data_criacao: datetime = "dd/MM/yyyy"
    observacao: List[ObservacaoViewSchema]
    produtos: List[ProdutoSchema]


class OrdemListViewSchema(BaseModel):
    """ Define como uma lista de ordens deverá ser representada.
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
        "obs": [{"id": obs.id, "texto": obs.texto,"data": obs.create_time.strftime(mascara)} for obs in ordem.observacao if not obs.deleted],
        "produtos": [{"nome": p.nome, "quantidade": p.quantidade} for p in ordem.produtos]
    }


def apresenta_ordens(ordens: List[Ordem]):
    """ Retorna uma representação de um conjunto de ordens seguindo o schema definido em
        OrdemListViewSchema.
    """
    
    
    mascara = "%d/%m/%Y %H:%M:%S"
    
    return {
        "ordens": [{
                "id": o.id,
                    "data_criacao": o.create_time.strftime(mascara),
                    "obs": [{"id": obs.id, "texto": obs.texto,"data": obs.create_time.strftime(mascara)} for obs in o.observacao if not obs.deleted],
                    "produtos": [{"nome": p.nome,"quantidade": p.quantidade} for p in o.produtos]} for o in ordens]
    }
from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto
from datetime import datetime


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Osso Bovino"
    quantidade: int = 12
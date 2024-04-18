from pydantic import BaseModel
from model.observacao import Observacao


class ObservacaoSchema(BaseModel):
    """ Define como uma nova observação a ser inserida deve ser representada
    """
    ordem_id: int = 1
    texto: str = "Lorem Ipsum"


class ObservacaoViewSchema(BaseModel):
    """ Define como uma observação deve ser apresentada
    """
    id: int = 1
    texto: str = "Lorem Ipsum"


class ObservacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


class ObservacaoBuscaSchema(BaseModel):
    """ Define como buscar uma observação.
    """
    obs_id: int = 0
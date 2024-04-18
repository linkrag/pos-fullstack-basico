from pydantic import BaseModel


class ProdutoSchema(BaseModel):
    """ Define como um novo produto deve ser inserido.
    """
    nome: str = "Osso Bovino"
    quantidade: int = 12
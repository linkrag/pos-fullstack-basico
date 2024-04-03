from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Ordem(Base):
    __tablename__ = 'ordempedido'
    
    id = Column("pk_ordempedido", Integer, primary_key=True)
    produto = Column(Integer, ForeignKey("produto.pk_produto"), nullable=False)
    create_time = Column(DateTime, default=datetime.now())    

    def __init__(self, produto:int, create_time:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.produto = produto
        if create_time:
            self.create_time = create_time
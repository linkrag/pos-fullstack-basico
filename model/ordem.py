from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from model.base import Base
from model.produto import Produto


class Ordem(Base):
    __tablename__ = 'ordem'
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=datetime.now)
    produtos = relationship("Produto")
    

    def adiciona_produto(self, produto:Produto):
        """ Adiciona um novo comentário ao Produto
        """
        self.produtos.append(produto)
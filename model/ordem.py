from sqlalchemy import Boolean, Column, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from model.base import Base
from model.observacao import Observacao

class Ordem(Base):
    __tablename__ = 'ordem'
    
    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now)
    produtos = relationship("Produto")
    observacao = relationship("Observacao")


    def adiciona_observacao(self, observacao:Observacao):
        """ Adiciona uma observação à ordem de produção
        """
        self.observacao.append(observacao)
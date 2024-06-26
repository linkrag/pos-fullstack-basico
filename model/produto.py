from sqlalchemy import *
from datetime import datetime

from model.base import Base


class Produto(Base):
    __tablename__ = 'produto'
    
    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    nome = Column(String(50), nullable=False)
    quantidade = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    ordem_id = Column(Integer, ForeignKey("ordem.id"), nullable=False)
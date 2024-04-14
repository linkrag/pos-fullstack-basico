from sqlalchemy import *
from datetime import datetime

from model.base import Base


class Observacao(Base):
    __tablename__ = 'observacao'

    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    texto = Column(String(4000), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    ordem_id = Column(Integer, ForeignKey("ordem.id"), nullable=False)
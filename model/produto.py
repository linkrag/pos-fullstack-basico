from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Ordem

class Produto(Base):
    __tablename__ = 'produto'
    
    id = Column("pk_produto", Integer, primary_key=True)
    product_name = Column(String(50), nullable=False,  unique=True)
    quantity = Column(Integer, nullable=False)
    #order_number = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now())    

    comentarios = relationship("Comentario")

    def __init__(self, product_name:str, 
                 quantity:int, 
                 #order_number:float,
                 create_time:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do produto.
            quantidade: quantidade que se espera comprar daquele produto
            valor: valor esperado para o produto
            data_insercao: data de quando o produto foi inserido à base
        """
        self.product_name = product_name
        self.quantity = quantity
        #self.order_number = order_number

        # se não for informada, será o data exata da inserção no banco
        if create_time:
            self.create_time = create_time

    def adiciona_comentario(self, ordem:Ordem):
        """ Adiciona um novo comentário ao Produto
        """
        self.comentarios.append(ordem)
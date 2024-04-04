from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Ordem
from logger import logger
from schemas.erro import *
from schemas.produto import *
from schemas.ordem import *
from flask_cors import CORS


info = Info(title="API Ordem de Serviço", version="0.2.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
ordem_tag = Tag(name="Ordem de produção", description="Adição e visualização de uma ordem de produção")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/ordem', tags=[ordem_tag],
           responses={"200": OrdemSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_order():
    """
    """
    logger.debug("Criando nova ordem de produção")
    data = request.json
    ordem = Ordem()
    for produto_data in data['produtos']:
        produto = Produto(nome=produto_data['nome'], quantidade=produto_data['quantidade'])
        ordem.produtos.append(produto)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(ordem)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_ordem(ordem), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = ""
        logger.warning(f"Erro ao criar ordem de produção {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Um erro aconteceu..."
        logger.warning(f"Erro ao criar uma ordem de produção {error_msg}")
        return {"mesage": error_msg}, 400
    

if __name__ == '__main__':
    app.run(debug=True)
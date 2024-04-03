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


info = Info(title="API Ordem de Serviço", version="1.0.0")
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


@app.post('/order', tags=[ordem_tag],
           responses={"200": OrdemSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_order(form: OrdemSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    ordem = List[ProdutoSchema]
    logger.debug("Adicionando ordem")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(ordem)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{ordem.nome}'")
        return apresenta_ordem(ordem), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{ordem.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pr*oduto '{ordem.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    

if __name__ == '__main__':
    app.run(debug=True)
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
           responses={"200": OrdemViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_order(body: OrdemSchema):
    """Cria uma nova ordem de produção com os produtos enviados
    
    Retorna uma representação da ordem de produção com os produtos associados.
    """
    logger.debug("Criando nova ordem 6de produção")
    ordem = Ordem()
    try:
        for produto in body.produtos:
            produto = Produto(nome=produto.nome, quantidade=produto.quantidade)
            ordem.produtos.append(produto)
            session = Session()
            session.add(ordem)
            session.commit()
            return apresenta_ordem(ordem), 200

    except IntegrityError as e:
        error_msg = e
        logger.warning(f"Erro ao criar ordem de produção {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = e
        logger.warning(f"Erro ao criar uma ordem de produção {error_msg}")
        return {"mesage": error_msg}, 400
    
    
@app.get('/ordem/<int:id>', tags=[ordem_tag],
           responses={"200": OrdemListViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_ordens(path: OrdemBuscaSchema):
    """Faz uma busca pelo ID informado no path ou pelo default 0
    
    Retorna todas as ordens de produção cadastradas, se o ID enviado for 0 (default), ou a ordem de produção do ID enviado.
    """
    try:
        session = Session()
        produto_id = path.id
        if produto_id != 0:
            ordens = session.query(Ordem).filter(Ordem.id == produto_id)
        else:
            ordens = session.query(Ordem).all()
        result = apresenta_ordens(ordens)
        session.close()
        return jsonify(result), 200

    except IntegrityError as e:
        error_msg = e
        logger.warning(f"Erro ao consultar a ordem de produção {e}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = e
        logger.warning(f"Erro ao consultar a ordem de produção {e}")
        return {"mesage": error_msg}, 400
    

if __name__ == '__main__':
    app.run(debug=True)
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify

from sqlalchemy.exc import IntegrityError

from model import Session, Ordem, Produto
from model.observacao import Observacao
from logger import logger
from schemas.erro import *
from schemas.ordem import *
from schemas.observacao import *    
from schemas.produto import *
from flask_cors import CORS


info = Info(title="API Ordem de Produção", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
ordem_tag = Tag(name="Ordem de produção", description="Adição, visualização e remoção de uma ordem de produção")
observacao_tag = Tag(name="Observação", description="Adição e remoção de produtos à ordem de produção")
produto_tag = Tag(name="Produto", description="Adição e remoção de produtos à ordem de produção")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/ordem/<int:ordem_id>', tags=[ordem_tag],
           responses={"200": OrdemListViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_ordens(path: OrdemBuscaSchema):
    """Faz uma busca pelo ID informado no path ou pelo default 0
    
    Retorna todas as ordens de produção cadastradas, se o ID enviado for 0 (default), ou a ordem de produção do ID enviado.
    """
    try:
        session = Session()
        #verifica o ID enviado
        if path.ordem_id != 0:
            ordens = session.query(Ordem).filter(Ordem.id == path.ordem_id)
        else:
            ordens = session.query(Ordem).filter(Ordem.deleted == False)
        result = apresenta_ordens(ordens)
        session.close()
        return jsonify(result), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao consultar a ordem de produção {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao consultar a ordem de produção {e.args}")
        return {"mesage": e.args}, 400
    
    
@app.put('/ordem', tags=[ordem_tag],
           responses={"200": OrdemViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_order(body: OrdemSchema):
    """Cria uma nova ordem de produção com os produtos enviados
    
    Retorna uma representação da ordem de produção com os produtos associados.
    """
    logger.debug("Criando nova ordem de produção")
    ordem = Ordem()
    try:
        for produto in body.produtos:
            novo_produto = Produto(nome=produto.nome, quantidade=produto.quantidade)
            produto_existente = False

            # Verificar se o produto já está na ordem
            for produto_ordem in ordem.produtos:
                if produto_ordem.nome == novo_produto.nome:
                    # Se o produto já estiver na ordem, apenas somar a quantidade
                    produto_ordem.quantidade += novo_produto.quantidade
                    produto_existente = True
                    break
            
            # Se o produto não estiver na ordem, adicione-o
            if not produto_existente:
                ordem.produtos.append(novo_produto)
        session = Session()
        session.add(ordem)
        session.commit()
        return apresenta_ordem(ordem), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao criar ordem de produção {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao criar ordem de produção {e.args}")
        return {"mesage": e.args}, 400


@app.delete('/ordem/<int:ordem_id>', tags=[ordem_tag],
            responses={"200": OrdemDelSchema, "404": ErrorSchema})
def del_ordem(path: OrdemBuscaSchema):
    """Deleta uma ordem de produção a partir de um ID informado no path

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        logger.debug(f"Deletando a ordem de produção #{path.ordem_id}")
        session = Session()
        ordem = session.query(Ordem).filter(Ordem.id == path.ordem_id).first()
        ordem.deleted = True
        session.commit()
        return {"mesage": "Ordem removida", "id": path.ordem_id}
        
    except IntegrityError as e:
        logger.warning(f"Erro ao excluir a ordem de produção {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao excluir a ordem de produção {e.args}")
        return {"mesage": e.args}, 400
    

@app.put('/obs', tags=[observacao_tag],
          responses={"200": OrdemViewSchema, "404": ErrorSchema})
def add_observacao(body: ObservacaoSchema):
    """Adiciona de uma nova observação a uma ordem na base identificada pelo id enviado

    Retorna uma representação da ordem de acordo com o schema de view da ordem.
    """
    try:
        ordem_id  = body.ordem_id
        session = Session()
        ordem = session.query(Ordem).filter(Ordem.id == ordem_id).first()

        if not ordem:
            error_msg = "Ordem não encontrada na base"
            logger.warning(f"Ocorreu um erro: '{ordem_id}', {error_msg}")
            return {"mesage": error_msg}, 404

        texto = body.texto
        observacao = Observacao()
        observacao.texto = texto
        ordem.adiciona_observacao(observacao)
        session.commit()
        return apresenta_ordem(ordem), 200
    
    except IntegrityError as e:
        logger.warning(f"Erro ao inserir a observação {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao inserir a observação {e.args}")
        return {"mesage": e.args}, 400


@app.delete('/obs/<int:obs_id>', tags=[observacao_tag],
            responses={"200": ObservacaoDelSchema, "404": ErrorSchema})
def del_observacao(path: ObservacaoBuscaSchema):
    """Deleta uma observação a partir do ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        logger.debug(f"Deletando a observação #{path.obs_id}")
        session = Session()
        observacao = session.query(Observacao).filter(Observacao.id == path.obs_id).first()
        observacao.deleted = True
        session.commit()
        return {"mesage": "Observação removida", "id": path.obs_id}
        
    except IntegrityError as e:
        logger.warning(f"Erro ao deletar a observação {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao deletar a observação {e.args}")
        return {"mesage": e.args}, 400
    
    
if __name__ == '__main__':  
   app.run(host='0.0.0.0', port=5003)